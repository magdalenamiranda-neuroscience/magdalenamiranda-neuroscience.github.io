(function () {
  document.querySelectorAll(".video").forEach(function (box) {
    var btn = box.querySelector(".video__play");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var f = document.createElement("iframe");
      f.src = box.dataset.embed;
      f.title = btn.getAttribute("aria-label").replace("Play video: ", "");
      f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
      f.referrerPolicy = "strict-origin-when-cross-origin";
      box.replaceChildren(f);
    });
  });
})();
