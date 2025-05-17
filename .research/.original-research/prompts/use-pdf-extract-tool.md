Use the @extract_full_pdf.py tool to extract the text from this file, following these steps:

1. First, check if the PDF file exists in the .research/pdfs/ directory. If it's in another location, move it there.

2. Before running the extraction, add appropriate frontmatter to the script for this PDF. Update the front_matter dictionary in extract_full_pdf.py with:
   - title: The full title of the document
   - creator: Author(s) name(s)
   - date: Publication date
   - format: Usually "Journal Article" for academic papers
   - subject: Brief description of the content
   - identifier: The document ID (often from JSTOR or other sources)
   - source: Full citation information including journal name, volume, issue, pages
   - topics: Relevant keywords separated by commas

3. Run the extraction script on the PDF using the proper command with the full path to the file.

4. After extraction, rename the file from its default name (usually something like "12345678-full.md") to a more descriptive filename using the following format:
   - Use lowercase letters
   - Replace spaces with hyphens
   - Include key subject matter in the name (e.g., "native-american-health-colonial-contact-maryland-full.md")
   - Keep the "-full.md" suffix

5. Verify that the extraction worked correctly by checking the content of the file.

This process ensures consistent, well-formatted, and descriptively named extracts of PDF documents in our research collection. 