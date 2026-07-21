#!/usr/bin/env node
/* Paste-ready HTML kaynagini KOPYA-YAPISTIR icin birebir koruyan Word dokumanina gomer.
   Word'un kivrik-tirnak/otomatik-duzeltme bozmasini onler (duz tirnaklar korunur).
   Kullanim: node build_docx.js <paste.html> <cikti.docx> "<Baslik>"
   docx global kurulu olmali:  npm install -g docx   (root: `npm root -g`) */
const fs = require("fs");
const { execSync } = require("child_process");
const G = execSync("npm root -g").toString().trim() + "/docx";
const { Document, Packer, Paragraph, TextRun, HeadingLevel, BorderStyle } = require(G);

const [,, srcPath, outPath, title] = process.argv;
const raw = fs.readFileSync(srcPath, "utf8");
const codeParas = raw.split("\n").map(line =>
  new Paragraph({ spacing: { after: 0, line: 240, lineRule: "auto" },
    children: [ new TextRun({ text: line.length ? line : " ", font: "Consolas", size: 15, color: "1a1a1a" }) ] }));

const doc = new Document({
  styles: { default: { document: { run: { font: "Arial", size: 22 } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 },
      margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 } } },
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1,
        children: [ new TextRun({ text: title || "Blog Enrichment", bold: true, size: 26 }) ] }),
      new Paragraph({ spacing: { after: 120 },
        children: [ new TextRun({ text: "Kullanim: Asagidaki kod blogunun TAMAMINI secip kopyalayin ve blog sayfasinin HTML / kaynak (source) duzenleyicisine yapistirin. Icerik metnine dokunmayin. FAQ semasi (JSON-LD) ayri dosyadadir; CMS <script> etiketini sildigi icin sayfanin schema alanina veya GTM'e eklenmelidir.",
          italics: true, size: 18, color: "5b6b7b" }) ] }),
      new Paragraph({ spacing: { after: 160 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "1a4290", space: 4 } }, children: [ new TextRun({ text: "", size: 4 }) ] }),
      ...codeParas,
    ],
  }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(outPath, buf); console.log("wrote", outPath, buf.length, "bytes"); });
