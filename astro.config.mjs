import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import starlightLinksValidator from "starlight-links-validator";
import tailwind from "@astrojs/tailwind";

export default defineConfig({
  site: "https://0bytes-security.github.io",
  base: "discovery-ce",
  integrations: [
    starlight({
      title: "Discovery",
      description: "Security Assessments Made Simple",
      components: {
        Header: "~/components/header.astro",
        Hero: "~/components/hero.astro",
        PageFrame: "~/components/page-frame.astro",
        TableOfContents: "~/components/table-of-contents.astro",
      },
      customCss: ["~/styles/tailwind.css"],
      plugins: [starlightLinksValidator({})],
      sidebar: [
        {
          label: "Overview",
          link: "/overview",
        },
        {
          label: "Architecture",
          link: "/architecture",
        },
      ],
      social: {
        github: "https://github.com/0bytes-security/discovery-ce",
      },
    }),
    tailwind({
      applyBaseStyles: false,
    }),
  ],
  server: {
    port: 1104,
  },
});
