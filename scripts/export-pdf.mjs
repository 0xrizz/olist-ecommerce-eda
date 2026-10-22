#!/usr/bin/env node
import { spawn } from 'node:child_process';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WEEK6_ROOT = path.resolve(__dirname, '..');
const INPUT_MD = path.resolve(WEEK6_ROOT, 'laporan-proyek-uts.md');
const STYLESHEET = path.resolve(WEEK6_ROOT, 'scripts/pdf-styles.css');
const TEMP_HTML = path.resolve('/tmp', 'bigdata_uts_report.html');
const OUTPUT_PDF = path.resolve(WEEK6_ROOT, 'laporan-proyek-uts.pdf');

function log(msg) {
  const ts = new Date().toISOString();
  console.log(`[${ts}] [export-pdf] ${msg}`);
}

function runCommand(cmd, args, cwd) {
  return new Promise((resolve, reject) => {
    log(`Executing: ${cmd} ${args.join(' ')} (cwd: ${cwd})`);
    const proc = spawn(cmd, args, { cwd, stdio: 'inherit' });
    proc.on('error', (err) => reject(new Error(`Failed to start ${cmd}: ${err.message}`)));
    proc.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`${cmd} exited with non-zero exit code: ${code}`));
      }
    });
  });
}

async function exportPdfPipeline() {
  log(`Starting UTS EDA PDF Export Pipeline...`);
  log(`Input Markdown: ${INPUT_MD}`);
  log(`Output PDF: ${OUTPUT_PDF}`);

  if (!fs.existsSync(INPUT_MD)) {
    throw new Error(`Input markdown file not found: ${INPUT_MD}`);
  }

  // 1. Convert Markdown to Standalone Embedded HTML using Pandoc
  log(`Step 1: Converting markdown to HTML with embedded assets via pandoc...`);
  const pandocArgs = [
    INPUT_MD,
    '-s',
    '--embed-resources',
    '--css', STYLESHEET,
    '-o', TEMP_HTML,
  ];
  await runCommand('pandoc', pandocArgs, WEEK6_ROOT);

  if (!fs.existsSync(TEMP_HTML)) {
    throw new Error(`Intermediate HTML generation failed: ${TEMP_HTML}`);
  }
  const htmlStats = fs.statSync(TEMP_HTML);
  log(`Generated HTML: ${TEMP_HTML} (${(htmlStats.size / 1024).toFixed(1)} KB)`);

  // 2. Render HTML to PDF using Headless Google Chrome
  log(`Step 2: Rendering HTML to PDF via Headless Google Chrome...`);
  const chromeArgs = [
    '--headless',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    `--print-to-pdf=${OUTPUT_PDF}`,
    '--no-pdf-header-footer',
    `file://${TEMP_HTML}`,
  ];
  await runCommand('google-chrome', chromeArgs, WEEK6_ROOT);

  if (!fs.existsSync(OUTPUT_PDF)) {
    throw new Error(`Chrome PDF generation failed: ${OUTPUT_PDF}`);
  }
  const rawStats = fs.statSync(OUTPUT_PDF);
  log(`Rendered Initial PDF: ${OUTPUT_PDF} (${(rawStats.size / (1024 * 1024)).toFixed(2)} MB)`);

  // 3. Post-process PDF via PyMuPDF (stamping running headers/footers & setting interactive TOC bookmarks)
  log(`Step 3: Post-processing PDF via PyMuPDF (stamping headers, footers & bookmarks)...`);
  const postArgs = [
    'run',
    '--with', 'pymupdf',
    'python3', 'scripts/postprocess-pdf.py',
    '--pdf', OUTPUT_PDF,
  ];
  await runCommand('uv', postArgs, WEEK6_ROOT);

  // 4. Verify Final Deliverable
  log(`Step 4: Verifying final PDF deliverable...`);
  const finalStats = fs.statSync(OUTPUT_PDF);
  const sizeMb = finalStats.size / (1024 * 1024);
  log(`Final PDF size: ${(finalStats.size / 1024).toFixed(1)} KB (~${sizeMb.toFixed(2)} MB)`);

  if (finalStats.size < 100 * 1024) {
    throw new Error(`PDF size suspiciously small (${finalStats.size} bytes).`);
  }
  if (finalStats.size > 10 * 1024 * 1024) {
    throw new Error(`PDF size (${sizeMb.toFixed(2)} MB) exceeds 10 MB limit.`);
  }

  // 5. Clean up temporary files
  if (fs.existsSync(TEMP_HTML)) {
    fs.unlinkSync(TEMP_HTML);
    log(`Cleaned up temporary HTML file.`);
  }

  log(`UTS EDA Report PDF export completed successfully: ${OUTPUT_PDF}`);
}

exportPdfPipeline()
  .then(() => process.exit(0))
  .catch((err) => {
    console.error(`[export-pdf:error] ${err.message}`);
    process.exit(1);
  });
