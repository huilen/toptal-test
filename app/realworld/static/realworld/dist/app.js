// Unpoly Settings
// ===============

// Enable unpoly config in browser console.
up.log.enable();

/* Automatically follow all links on a page without requiring an [up-follow] attribute and
without refreshing whole page. */
up.link.config.followSelectors.push("a[href]");

/* Automatically follow all links on a page without requiring an [up-instant] attribute and
followed on mousedown instead of on click. */
up.link.config.instantSelectors.push("a[href]");

/* Automatically follow all forms on a page without requiring an [up-submit] attribute and
without refreshing whole page after submitting. */
up.form.config.submitSelectors.push(["form"]);

// Let unpoly render page from [.wrapper] class instead of [main] html tag.
up.fragment.config.mainTargets = ".wrapper";

// Disable inputs and buttons when Form submit.
up.on("up:form:submit", () => {
  document.querySelectorAll('button[type=submit], fieldset').forEach((element) => {
    element.disabled = true;
  })
});
