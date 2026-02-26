"""
Git operations for automated commits and pushes
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple


class GitManager:
    """Manage git operations for the pipeline"""
    
    def __init__(
        self,
        repo_path: str = ".",
        branch: str = "main",
        auto_commit: bool = True,
        auto_push: bool = True
    ):
        self.repo_path = Path(repo_path).resolve()
        self.branch = branch
        self.auto_commit = auto_commit
        self.auto_push = auto_push
    
    def _run_command(
        self,
        args: List[str],
        check: bool = True
    ) -> Tuple[int, str, str]:
        """Run a git command and return exit code, stdout, stderr"""
        result = subprocess.run(
            ["git"] + args,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    
    def is_git_repo(self) -> bool:
        """Check if the path is a git repository"""
        code, _, _ = self._run_command(["rev-parse", "--is-inside-work-tree"], check=False)
        return code == 0
    
    def get_current_branch(self) -> Optional[str]:
        """Get the current branch name"""
        code, stdout, _ = self._run_command(["rev-parse", "--abbrev-ref", "HEAD"], check=False)
        return stdout if code == 0 else None
    
    def get_status(self) -> Tuple[List[str], List[str]]:
        """
        Get git status.
        Returns (staged_files, modified_files)
        """
        code, stdout, _ = self._run_command(["status", "--porcelain"], check=False)
        
        staged = []
        modified = []
        
        if code == 0 and stdout:
            for line in stdout.split('\n'):
                if not line:
                    continue
                
                status = line[:2]
                filepath = line[3:]
                
                if status[0] in 'MADRC':
                    staged.append(filepath)
                if status[1] in 'MD':
                    modified.append(filepath)
        
        return staged, modified
    
    def has_changes(self) -> bool:
        """Check if there are any changes to commit"""
        staged, modified = self.get_status()
        return len(staged) > 0 or len(modified) > 0
    
    def add_files(self, files: Optional[List[str]] = None) -> bool:
        """
        Stage files for commit.
        If files is None, stages all changes.
        """
        if files:
            code, _, stderr = self._run_command(["add"] + files, check=False)
        else:
            code, _, stderr = self._run_command(["add", "."], check=False)
        
        return code == 0
    
    def commit(
        self,
        message: str,
        allow_empty: bool = False
    ) -> Tuple[bool, Optional[str]]:
        """
        Create a commit.
        Returns (success, commit_hash)
        """
        args = ["commit", "-m", message]
        if allow_empty:
            args.append("--allow-empty")
        
        code, stdout, stderr = self._run_command(args, check=False)
        
        if code != 0:
            return False, None
        
        code, stdout, _ = self._run_command(["rev-parse", "HEAD"], check=False)
        commit_hash = stdout[:7] if code == 0 else None
        
        return True, commit_hash
    
    def push(
        self,
        remote: str = "origin",
        branch: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Push to remote repository.
        Returns (success, message)
        """
        target_branch = branch or self.branch
        code, stdout, stderr = self._run_command(
            ["push", remote, target_branch],
            check=False
        )
        
        if code == 0:
            return True, f"Pushed to {remote}/{target_branch}"
        return False, stderr or "Push failed"
    
    def pull(self, remote: str = "origin", branch: Optional[str] = None) -> bool:
        """Pull latest changes from remote"""
        target_branch = branch or self.branch
        code, _, _ = self._run_command(["pull", remote, target_branch], check=False)
        return code == 0
    
    def auto_deploy(
        self,
        files: Optional[List[str]] = None,
        message_template: str = "chore(seo): update SEO content - {timestamp}"
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Automatically add, commit, and push changes.
        Returns (success, message, commit_hash)
        """
        if not self.is_git_repo():
            return False, "Not a git repository", None
        
        if not self.has_changes():
            return True, "No changes to commit", None
        
        if not self.add_files(files):
            return False, "Failed to stage files", None
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = message_template.format(timestamp=timestamp)
        
        success, commit_hash = self.commit(message)
        if not success:
            return False, "Failed to create commit", None
        
        if self.auto_push:
            success, push_msg = self.push()
            if not success:
                return False, f"Commit created but push failed: {push_msg}", commit_hash
        
        return True, f"Successfully committed and pushed", commit_hash
    
    def get_last_commit_info(self) -> Optional[dict]:
        """Get information about the last commit"""
        code, stdout, _ = self._run_command(
            ["log", "-1", "--format=%H|%an|%ae|%s|%ci"],
            check=False
        )
        
        if code != 0 or not stdout:
            return None
        
        parts = stdout.split('|')
        if len(parts) >= 5:
            return {
                "hash": parts[0],
                "author": parts[1],
                "email": parts[2],
                "message": parts[3],
                "date": parts[4]
            }
        
        return None
