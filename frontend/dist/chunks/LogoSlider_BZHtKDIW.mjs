import { c as createComponent, m as maybeRenderHead, b as addAttribute, a as renderTemplate } from './astro/server_Dk78qWC5.mjs';
import 'piccolore';
import 'html-escaper';
import 'clsx';
/* empty css                            */

const $$LogoSlider = createComponent(($$result, $$props, $$slots) => {
  const logos = [
    { name: "Salesforce", url: "https://www.salesforce.com", img: "https://cdn.simpleicons.org/salesforce" },
    { name: "HubSpot", url: "https://www.hubspot.com", img: "https://cdn.simpleicons.org/hubspot" },
    { name: "Zendesk", url: "https://www.zendesk.com", img: "https://cdn.simpleicons.org/zendesk" },
    { name: "Slack", url: "https://slack.com", img: "https://cdn.simpleicons.org/slack" },
    { name: "Microsoft", url: "https://www.microsoft.com", img: "https://cdn.simpleicons.org/microsoft" },
    { name: "Zoom", url: "https://zoom.us", img: "https://cdn.simpleicons.org/zoom" }
  ];
  return renderTemplate`${maybeRenderHead()}<section class="section section-alt hide-on-mobile" data-astro-cid-os5rwseq> <div class="container" data-astro-cid-os5rwseq> <div class="section-header" data-astro-cid-os5rwseq> <h2 data-astro-cid-os5rwseq>Seamless <span class="text-gradient-primary" data-astro-cid-os5rwseq>Integrations</span></h2> <p data-astro-cid-os5rwseq>Connect My Call Connect with your favorite tools and build custom workflows with our powerful API</p> </div> <!-- Integration Logos Slider --> <div class="logo-slider" data-astro-cid-os5rwseq> <div class="logo-track" data-astro-cid-os5rwseq>  ${logos.map((logo) => renderTemplate`<a${addAttribute(logo.url, "href")} target="_blank" rel="noopener noreferrer" class="logo-item"${addAttribute(logo.name, "title")} data-astro-cid-os5rwseq> <img${addAttribute(logo.img, "src")}${addAttribute(logo.name, "alt")} class="logo-img" width="40" height="40" data-astro-cid-os5rwseq> </a>`)}  ${logos.map((logo) => renderTemplate`<a${addAttribute(logo.url, "href")} target="_blank" rel="noopener noreferrer" class="logo-item" aria-hidden="true" tabindex="-1" data-astro-cid-os5rwseq> <img${addAttribute(logo.img, "src")}${addAttribute(logo.name, "alt")} class="logo-img" width="40" height="40" data-astro-cid-os5rwseq> </a>`)}  ${logos.map((logo) => renderTemplate`<a${addAttribute(logo.url, "href")} target="_blank" rel="noopener noreferrer" class="logo-item" aria-hidden="true" tabindex="-1" data-astro-cid-os5rwseq> <img${addAttribute(logo.img, "src")}${addAttribute(logo.name, "alt")} class="logo-img" width="40" height="40" data-astro-cid-os5rwseq> </a>`)}  ${logos.map((logo) => renderTemplate`<a${addAttribute(logo.url, "href")} target="_blank" rel="noopener noreferrer" class="logo-item" aria-hidden="true" tabindex="-1" data-astro-cid-os5rwseq> <img${addAttribute(logo.img, "src")}${addAttribute(logo.name, "alt")} class="logo-img" width="40" height="40" data-astro-cid-os5rwseq> </a>`)} </div> </div> </div> </section> `;
}, "C:/Users/User/Documents/trae_projects/mycallconnect/frontend/src/components/LogoSlider.astro", void 0);

export { $$LogoSlider as $ };
