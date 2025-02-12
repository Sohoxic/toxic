# toxic

Welcome to Toxic by [Sohoxic](https://github.com/Sohoxic/toxic), a simple and minimal static site generator which was primarily designed to help me easily document my life by keeping notes, learnings, thoughts all in one place instead of making static website for everything everytime, thus prioritising easy website building. This is the gardener of my digital garden(the initiator and the master to convert markdown files to static websites.).

For my fellow develops who wants to transform their lives in the similar way which I did, here's toxic for you to document your life, learnings etc. 

> Why Choose Toxic? 
> If your focus is more on content rather than configuration, then toxic is for you

## The Philosophy Behind Toxic

Toxic was created with three core principles in mind:

* **Simplicity**: No unnecessary complexity or bloat. You should be painlessly able to write `.md` files without having to worry about setting up and using your ssg.
* **Performance**: Ease of use should be the priority with faster processing and build times. We have parallel processing in place to take care of this
* **Aesthetics**: Tokyonight theme. I love this! If you don't you can always customise, toxic has given you all the flexibility

> Toxic does all of this, with style. Haha!

[Get started with Toxic Today!](https://github.com/Sohoxic/toxic) 

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Project Structure

```
your-site/
├── toxic.py          # The static site generator script
├── content/             # Your markdown files go here
├── templates/           # HTML templates
├── assets/             # Static assets (CSS, images, etc.)
│   └── css/
│       └── style.css
└── dist/               # Generated site (output directory)
```

<!-- ## Key Features

Here's what makes Toxic special:

* **Dark Theme First**: Carefully crafted dark color scheme that reduces eye strain 😜
* **Lightning Fast**: Built with Python for optimal performance (supports parallel processing of md files)
* **Smart Defaults**: Pre-configured with Roboto Mono for excellent readability.
* **Responsive design**
* **Quick rebuild times**
* **Code syntax highlighting**
* **YAML frontmatter support** -->



## Installation

1. Clone this repository or download the files:
```bash
git clone https://github.com/Sohoxic/toxic.git
cd toxic
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Create a New Post

Create a markdown file in the `content` directory with YAML frontmatter:

```markdown
---
title: My First Post
template: default.html
---

# Welcome to My Blog

This is my first blog post.
```

### 2. Build the Site

Run the generator:
```bash
python toxic.py
```

### 3. View Your Site

Open `dist/your-post.html` in a web browser to see your generated page.

## Customization Options

### Modifying the Theme

The dark theme CSS is located in `assets/css/style.css`. You can modify:
* Color schemes
* Typography
* Layout structure


### Template Customization

Modify `templates/default.html` to change the HTML structure.


## Technical Details

Here's a breakdown of Toxic's key components:

| Component | Technology | Purpose |
|-----------|------------|----------|
| Parser | Python-Markdown | Content Processing |
| Templates | Jinja2 | Layout Generation |
| Styling | Modern CSS | Visual Presentation |
| Configuration | YAML | Site Customization |
| Build System | Python | Site Generation |

## Deployment

### GitHub Pages

1. Create a new repository on GitHub
2. Push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```
3. Enable GitHub Pages in repository settings
4. Set the source to the `dist` directory

### Netlify

1. Create a `netlify.toml`:
```toml
[build]
  publish = "dist"
  command = "python generator.py"
```
2. Connect your repository to Netlify
3. Deploy!

### Vercel

1. Create a `vercel.json`:
```json
{
  "buildCommand": "python toxic.py",
  "outputDirectory": "dist"
}
```
2. Connect your repository to Vercel
3. Deploy!







> `toxic` gives you the power to create without getting in your way. It's the static site generator that developers have been waiting for.

Remember, `toxic` is more than just a static site generator - it's a complete solution for developers who appreciate the elegance of dark themes and the power of simplicity.

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this in your own projects!
