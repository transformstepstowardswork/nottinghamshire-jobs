# Editing articles and activities

Open Pages CMS with your authorised editor account and select this repository and its publishing branch. Choose **Articles — English**, **文章 — 繁體中文**, **Activities — English** or **活動 — 繁體中文**. These are independent collections: publishing in one language does not create or translate an entry in the other.

Choose **New** to create an entry, or open an existing entry to edit or delete it. Add a title and the available details. For an activity, leave unknown dates, times, cost and other details blank; use 24-hour `HH:MM` times in London local time. Unknown cost is displayed as unspecified. Add the main text in the rich-text editor; headings, lists, links and inline images can be added there. Use an `https://` or `http://` address for registration links.

For an article, add one or more topics using the repeatable topic field, one topic per item. Enter the words without `#`; the site adds it. Readers can select topics on that language's article archive. Leave the field empty when no topic is needed.

Choose an image from the image picker or upload one. Use a common web image (JPEG, PNG, WebP or GIF), a descriptive filename and a reasonably small file; add a clear image description in the alt-text field. Add a description to inline images too. A cover without an image description is not displayed. The CMS stores uploaded images in this repository.

Save the entry. **Save creates a Git commit; it does not prove the site built or published successfully.** Check the repository's Pages build in GitHub Actions, then open the published archive and the entry's link in the intended language. A new item receives a stable filename; changing its title does not change that address. Entries with the same title remain separate. If the build reports an editorial HTML error, remove the unsafe link or unsupported raw HTML and save again; ordinary headings, lists, links and images are supported.

If an entry is missing, check that you selected the intended language, saved it on the publishing branch, and that the Pages build succeeded. Check required fields, image descriptions and web addresses. A failed build needs correction before it can appear. Deleting an entry removes it on the next successful build; check the public link afterwards. If the CMS or build reports an error you cannot resolve, keep the error message and ask for help.

The repository and its content, including drafts committed there, are not private. Do not put sensitive or personal information in an entry or image.

## Verified publication

Articles and Activities use the established `Publish verified Pages` workflow. An approved change reaching `main` triggers a build, verification of the generated pages, and deployment of that same checked output. Routine editing does not require repeating the original commissioning steps or changing Pages settings or App permissions.

Check the workflow for the exact saved or merged `main` revision, then open the public archive and entry. A save on another branch does not publish until the approved change reaches `main`; a failed verification needs correction before publication. See the [publishing and recovery runbook](PAGES_RUNBOOK.md) for failures and recovery. CMS editing does not manage the weekly Jobs feed.
