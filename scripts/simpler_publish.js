// Simple script to publish the next scheduled post during Netlify build
// This avoids the complexity of GitHub Actions and SSH keys

const fs = require('fs');
const path = require('path');

// Directory paths
const draftsDir = path.join(__dirname, '../drafts/english/press');
const contentDir = path.join(__dirname, '../content/english/press');

// Ensure directories exist
if (!fs.existsSync(draftsDir)) {
  console.log('Creating drafts directory');
  fs.mkdirSync(draftsDir, { recursive: true });
}

if (!fs.existsSync(contentDir)) {
  console.log('Creating content directory');
  fs.mkdirSync(contentDir, { recursive: true });
}

// Function to check if we should publish a post today
function shouldPublishToday() {
  const today = new Date();
  
  // Publish only on Sundays (day 0)
  if (today.getDay() !== 0) {
    console.log(`Today is not Sunday, skipping publication`);
    return false;
  }
  
  return true;
}

// Find all draft posts
let draftPosts = [];
try {
  if (fs.existsSync(draftsDir)) {
    const files = fs.readdirSync(draftsDir);
    
    for (const file of files) {
      if (file.endsWith('.md')) {
        const filePath = path.join(draftsDir, file);
        const content = fs.readFileSync(filePath, 'utf8');
        
        // Check if it's a draft
        if (content.includes('draft: true')) {
          // Extract the date
          const dateMatch = content.match(/date:\s*(\d{4}-\d{2}-\d{2})/);
          if (dateMatch && dateMatch[1]) {
            draftPosts.push({
              path: filePath,
              date: new Date(dateMatch[1]),
              filename: file
            });
          }
        }
      }
    }
  }
} catch (error) {
  console.error('Error reading draft posts:', error);
}

// Sort by date (oldest first)
draftPosts.sort((a, b) => a.date - b.date);

// Publish the oldest post if we should publish today
if (draftPosts.length > 0 && shouldPublishToday()) {
  const nextPost = draftPosts[0];
  console.log(`Publishing post: ${nextPost.filename}`);
  
  // Read the content
  let content = fs.readFileSync(nextPost.path, 'utf8');
  
  // Update draft status
  content = content.replace('draft: true', 'draft: false');
  
  // Update date to today
  const today = new Date().toISOString().split('T')[0];
  content = content.replace(/date:\s*\d{4}-\d{2}-\d{2}/, `date: ${today}`);
  
  // Write to content directory
  const targetPath = path.join(contentDir, nextPost.filename);
  fs.writeFileSync(targetPath, content);
  
  // Delete from drafts directory
  fs.unlinkSync(nextPost.path);
  
  console.log(`Successfully published ${nextPost.filename} with date ${today}`);
} else {
  console.log('No posts to publish today');
} 