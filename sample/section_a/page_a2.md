# Advanced Features

## Custom Styling

HVYM Press allows you to customize the look and feel of your site with ease.

### Adding Custom CSS

1. Create a `custom.css` file in your project directory
2. Add your custom styles
3. Link it in your template

```css
/* custom.css */
body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #333;
}

h1, h2, h3 {
    color: #2c3e50;
    margin-top: 1.5em;
}
```

## Using Components

### Cards

Create beautiful card layouts:

```markdown
::: card
## Feature One
Description of the first feature
:::

::: card
## Feature Two
Description of the second feature
:::
```

## Advanced Markdown

### Tables

| Feature | Description | Status |
|---------|-------------|--------|
| IPFS Deployment | Deploy to the decentralized web | ✅ |
| Custom Domains | Use your own domain | ✅ |
| Analytics | Built-in visitor tracking | Coming Soon |

### Code Blocks with Syntax Highlighting

```python
def hello_world():
    print("Hello, HVYM Press!")
    return True
```

## Deployment Options

1. **IPFS** - Decentralized hosting
2. **GitHub Pages** - Free static hosting
3. **Netlify** - Advanced CI/CD pipeline
4. **Vercel** - Serverless deployment

---
*Next: [Section B: Real-world Examples](section_b/page_b1.html)*
