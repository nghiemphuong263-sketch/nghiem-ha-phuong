# Add a blog post

Edit `blog/posts.json` and add an object in the array:

```json
[
  {
    "slug": "your-post-title",
    "title": "Your post title",
    "category": "Research",
    "date": "2026-10-27",
    "excerpt": "A short introduction.",
    "paragraphs": ["First paragraph.", "Second paragraph."],
    "published": true
  }
]
```

Use a unique slug with letters, numbers and hyphens. Set `published` to false to keep a post hidden. Upload the updated folder to Netlify, or commit it to your connected repository. The blog currently has no published posts.
