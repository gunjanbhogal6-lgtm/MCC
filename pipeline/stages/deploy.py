"""
Stage 4: Deploy - Git commit and push changes
"""

from dataclasses import dataclass, field
from typing import List, Optional

from ..utils.config import get_config
from ..utils.git_manager import GitManager
from ..utils.logger import get_logger


@dataclass
class DeployResult:
    """Result of the deploy stage"""
    success: bool
    committed: bool = False
    pushed: bool = False
    commit_hash: Optional[str] = None
    commit_message: Optional[str] = None
    files_changed: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class DeployStage:
    """Stage 4: Deploy changes via git"""
    
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger()
        self.git_manager = GitManager(
            branch=self.config.git_branch,
            auto_commit=self.config.auto_commit,
            auto_push=self.config.auto_push
        )
    
    def run(
        self,
        files: Optional[List[str]] = None,
        commit_message: Optional[str] = None,
        dry_run: bool = False
    ) -> DeployResult:
        """
        Run the deploy stage.
        
        Args:
            files: Specific files to commit (None = all changes)
            commit_message: Custom commit message
            dry_run: If True, don't actually commit/push
            
        Returns:
            DeployResult with deployment information
        """
        self.logger.stage("DEPLOY", "Starting git deployment...")
        
        result = DeployResult(success=False)
        
        if not self.git_manager.is_git_repo():
            result.errors.append("Not a git repository")
            return result
        
        staged, modified = self.git_manager.get_status()
        result.files_changed = staged + modified
        
        if not result.files_changed:
            self.logger.info("No changes to deploy")
            result.success = True
            result.committed = True
            result.pushed = True
            return result
        
        self.logger.info(f"Files to commit: {len(result.files_changed)}")
        for f in result.files_changed[:5]:
            self.logger.info(f"  - {f}")
        if len(result.files_changed) > 5:
            self.logger.info(f"  ... and {len(result.files_changed) - 5} more")
        
        if dry_run:
            self.logger.info("Dry run - skipping commit and push")
            result.success = True
            return result
        
        message_template = self.config.get(
            'git', 'commit_message_template',
            default="chore(seo): update SEO content - {timestamp}"
        )
        
        if commit_message:
            message = commit_message
        else:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = message_template.format(timestamp=timestamp)
        
        result.commit_message = message
        
        success, msg, commit_hash = self.git_manager.auto_deploy(
            files=files,
            message_template=message if not commit_message else commit_message
        )
        
        if success:
            result.success = True
            result.committed = True
            result.pushed = self.config.auto_push
            result.commit_hash = commit_hash
            
            if commit_hash:
                self.logger.success(f"Committed: {commit_hash}")
            if self.config.auto_push:
                self.logger.success("Changes pushed to remote")
        else:
            result.errors.append(msg)
            self.logger.error(f"Deployment failed: {msg}")
        
        return result
    
    def get_status(self) -> dict:
        """Get current git status"""
        if not self.git_manager.is_git_repo():
            return {"is_repo": False}
        
        staged, modified = self.git_manager.get_status()
        branch = self.git_manager.get_current_branch()
        last_commit = self.git_manager.get_last_commit_info()
        
        return {
            "is_repo": True,
            "branch": branch,
            "staged_files": staged,
            "modified_files": modified,
            "has_changes": bool(staged or modified),
            "last_commit": last_commit
        }
