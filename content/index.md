---
title: "Soham Sarkar - AI, Systems, Research"
template: home.html

# Hero Section Customization
hero_title: "Hey, I'm Soham! 👋"
hero_subtitle: "Welcome to my corner of the internet. Here's a little about my journey so far."

# Social Links
github_url: "https://github.com/soham-sarkar"
twitter_url: "https://twitter.com/soham_sarkar"
linkedin_url: "https://linkedin.com/in/soham-sarkar"

# Timeline Section
timeline_title: "What I've Been Up To"
timeline_subtitle: "A quick rundown of the stuff I've done over the years"

# Custom Timeline Items (optional - if not provided, defaults will be used)
timeline_items:
  - year: "2025"
    achievements:
      - "Started building personal projects and exploring AI/ML"
      - "Focusing on systems programming and distributed systems"
  - year: "2024"
    achievements:
      - "Completed Bachelor's in Computer Science"
  - year: "2023"
    achievements:
      - "Advanced studies in computer science"
      - "Worked on various programming projects"
  - year: "2022"
    achievements:
      - "Deepened understanding of computer science fundamentals"
  - year: "2021"
    achievements:
      - "Started my Bachelor's in Computer Science unaware of anything about tech"
  - year: "2018-2020"
    achievements:
      - "Class 10 (Matriculation) - Core subjects including Science and Mathematics - 94.6%"
      - "Class 12 (Higher Secondary) - Science stream (Physics, Chemistry, Mathematics) - 93.6%"

# Call-to-Action Section
cta_title: "Ready to dive deeper?"
cta_subtitle: "Explore my thoughts on AI, systems, research, and everything in between."
cta_link: "/blog/"
cta_button_text: "Read My Blog →"
---

# Welcome to My Personal Site

This markdown content can be used if you want to include additional content below the main home page sections. The home template will render all the sections above based on the frontmatter variables, and any markdown content here will be available as `{{ content | safe }}` in the template if you choose to use it.

You can customize every aspect of the home page by modifying the frontmatter variables above:

- **Hero Section**: Change the title and subtitle
- **Social Links**: Update your social media URLs
- **Timeline**: Modify the timeline items, years, and achievements
- **Call-to-Action**: Customize the CTA section text and links

The template uses Jinja2's `default()` filter, so if you don't specify a variable, it will use sensible defaults. 