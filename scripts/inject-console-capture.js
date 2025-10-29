# scripts/inject-console-capture.js
const fs = require('fs');
const path = require('path');
const glob = require('glob');

const SCRIPT_TAG = '<script src="/dashboard-console-capture.js"></script>';
const COMMENT = '<!-- Console capture script for dashboard debugging -->';

function injectConsoleCapture() {
  try {
    // Find all HTML files in common output directories
    const patterns = [
      'dist/**/*.html',
      'build/**/*.html',
      'out/**/*.html',
      '_site/**/*.html',
      'public/**/*.html',
      '*.html'
    ];
    
    let filesProcessed = 0;
    
    patterns.forEach(pattern => {
      const files = glob.sync(pattern, { ignore: 'node_modules/**' });
      
      files.forEach(filePath => {
        try {
          let content = fs.readFileSync(filePath, 'utf8');
          
          // Skip if script already injected
          if (content.includes('dashboard-console-capture.js')) {
            return;
          }
          
          // Try to inject in head
          if (content.includes('</head>')) {
            content = content.replace('</head>', `  ${COMMENT}\n  ${SCRIPT_TAG}\n</head>`);
          } 
          // Fallback: inject at start of body
          else if (content.includes('<body>')) {
            content = content.replace('<body>', `<body>\n  ${COMMENT}\n  ${SCRIPT_TAG}`);
          }
          // Fallback: inject after opening html tag
          else if (content.includes('<html>')) {
            content = content.replace('<html>', `<html>\n${COMMENT}\n${SCRIPT_TAG}`);
          }
          
          fs.writeFileSync(filePath, content);
          filesProcessed++;
          console.log(`✅ Injected console capture into: ${filePath}`);
        } catch (error) {
          console.error(`❌ Error processing ${filePath}:`, error.message);
        }
      });
    });
    
    if (filesProcessed === 0) {
      console.log('ℹ️ No HTML files found to process for console capture injection.');
    } else {
      console.log(`✅ Console capture injection complete. Processed ${filesProcessed} files.`);
    }
    
  } catch (error) {
    console.error('❌ Error during console capture injection:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  injectConsoleCapture();
}

module.exports = injectConsoleCapture;