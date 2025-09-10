# Deployment & Advanced Features

## IPFS Deployment

HVYM Press makes it easy to deploy your site to the InterPlanetary File System (IPFS).

### Quick Deployment

```bash
# Build your site
hvym-press build

# Deploy to IPFS
hvym-press deploy --ipfs
```

### Custom Domains

Point your domain to your IPFS content:

1. Add a DNS TXT record with your domain provider
2. Update your DNS settings
3. Configure your site's `config.json`

```json
{
  "site": {
    "domain": "example.com",
    "ipns": "k51qaz..."
  }
}
```

## Environment Variables

Use environment variables for sensitive information:

```env
API_KEY=your_api_key_here
ANALYTICS_ID=UA-XXXXX
```

Access them in your templates:

```html
<script>
  const apiKey = '{{ env.API_KEY }}';
  const analyticsId = '{{ env.ANALYTICS_ID }}';
</script>
```

## Custom Build Scripts

Add custom build steps in `package.json`:

```json
{
  "scripts": {
    "build": "hvym-press build",
    "deploy": "npm run build && hvym-press deploy",
    "preview": "hvym-press serve --port 3000"
  }
}
```

## SEO Optimization

### Meta Tags

Add SEO meta tags to your pages:

```yaml
---
title: My Awesome Page
description: A comprehensive guide to HVYM Press
author: Your Name
image: /_resources/og-image.jpg
---
```

### Sitemap Generation

HVYM Press automatically generates a sitemap.xml for your site.

## Performance Tips

1. **Image Optimization**
   - Use WebP format
   - Specify image dimensions
   - Use responsive images

2. **Code Splitting**
   - Split large JavaScript bundles
   - Lazy load non-critical resources

3. **Caching**
   - Leverage browser caching
   - Use service workers for offline support

## Advanced Configuration

### Custom Build Pipeline

```javascript
// build.js
const { build } = require('hvym-press');
const imagemin = require('imagemin');

async function customBuild() {
  // Run the default build
  await build();
  
  // Add custom optimizations
  await imagemin(['dist/_resources/*.{jpg,png}'], {
    destination: 'dist/_resources/optimized',
    plugins: [
      require('imagemin-mozjpeg')({ quality: 80 }),
      require('imagemin-pngquant')({ quality: [0.6, 0.8] })
    ]
  });
}

customBuild();
```

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check for syntax errors in markdown
   - Verify all dependencies are installed
   - Check file permissions

2. **Deployment Issues**
   - Verify API keys and credentials
   - Check network connectivity
   - Review deployment logs

### Getting Help

- [Documentation](https://github.com/inviti8/hvym_press)
- [GitHub Issues](https://github.com/inviti8/hvym_press/issues)
- [Community Forum](#)

---
*Back to [Home](/)*
