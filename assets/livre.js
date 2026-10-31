/* « Li trô d' chèrpint » — on tourne les pages au clic, comme un feuillet. */
(function () {
  "use strict";
  var D = window.LIVRE, M = D.meta, P = D.pages, NOTES = {};
  D.notes.forEach(function (n) { NOTES[String(n.n)] = n.texte; });

  var livre = document.getElementById("pages"),
      total = P.length + 2,            // couverture + 13 pages + colophon
      idx = -1, pages = [];   // -1 : aucune page montee, sinon va(0) sortirait aussitot

  /* ------------------------------------------------------------- fabrique */
  function el(t, cls, html) {
    var e = document.createElement(t);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function notesDe(p) {
    var ids = [], re = /data-note="(\d+)"/g, m;
    while ((m = re.exec(p.wa))) ids.push(m[1]);
    if (!ids.length) return "";
    return '<div class="notes">' + ids.map(function (i) {
      return "<p>" + i + ". " + NOTES[i] + "</p>";
    }).join("") + "</div>";
  }

  function pageConte(p) {
    var a = el("article", "page" + (p.citation ? " citation" : ""));
    a.innerHTML =
      '<div class="entete"><span class="titre-page">' + p.titre_wa +
      ' &nbsp;·&nbsp; <span>' + p.titre_fr + '</span></span>' +
      '<span class="folio">' + p.n + " / " + P.length + "</span></div>" +
      '<div class="planche"><img src="illustrations/' + p.illus + '.svg" alt="" loading="lazy"></div>' +
      '<div class="textes">' +
        '<div class="col-wa"><div class="langue">Wallon</div>' +
          '<p class="wa corps" lang="wa">' + p.wa + "</p></div>" +
        '<div class="filet"></div>' +
        '<div class="col-fr"><div class="langue">Français</div>' +
          '<p class="fr corps" lang="fr">' + p.fr + "</p></div>" +
        notesDe(p) +
      "</div>";
    return a;
  }

  function couverture() {
    var a = el("article", "page couverture");
    a.innerHTML =
      '<div class="serie">' + M.serie + "</div>" +
      '<h1 class="grand-titre" lang="wa">' + M.titre_wa + "</h1>" +
      '<p class="sous-titre" lang="fr">' + M.titre_fr + "</p>" +
      '<div class="planche"><img src="illustrations/00-couverture.svg" alt=""></div>' +
      '<p class="credit">Légende recueillie par <b>' + M.auteur_fr + "</b><br>" +
      "Traduction wallonne de <b>" + M.auteur_wa + "</b></p>" +
      '<button class="ouvrir" type="button">Ouvrir le livre</button>';
    a.querySelector(".ouvrir").addEventListener("click", function (e) {
      e.stopPropagation(); va(1);
    });
    return a;
  }

  function colophon() {
    var a = el("article", "page colophon");
    a.innerHTML =
      "<h2>Li trô d’ chèrpint</h2>" +
      '<p style="font-style:italic;color:var(--ocre)">Le trou du serpent</p>' +
      '<div class="colophon-grille">' +
        "<div><h3>Le texte</h3>" +
          "<p>Légende recueillie et mise en français par <b>" + M.auteur_fr + "</b>, " +
          "traduite en wallon par <b>" + M.auteur_wa + "</b>.</p>" +
          "<p>Paru dans <b>" + M.source + "</b>, sous le titre de série « " + M.serie + " ».</p>" +
          "<p>La légende a sûrement été contée en wallon. Laport l’a fixée en français, comme le faisaient les folkloristes de son temps ; la traduction d’Henri Grandry la ramène, quatre-vingts ans plus tard, dans la langue où on la racontait.</p></div>" +
        "<div><h3>Georges Laport</h3>" +
          "<p>Né à Fraiture en 1898, mort au camp de Dachau en 1945. Homme de lettres, critique d’art et historien des traditions populaires, il fut l’un des pionniers de l’enquête orale en Wallonie et recueillit des récits qui, sans lui, auraient disparu.</p>" +
          "<p>On lui doit notamment <i>Le folklore des paysages de Wallonie</i> (1929) et <i>Les contes populaires wallons</i> (1932). Membre de la Société de littérature wallonne et de la Commission nationale de folklore, il entra en résistance dès le début de la guerre, fut arrêté le 4 juin 1942 et déporté.</p>" +
          "<p>Son œuvre est dans le domaine public depuis 2016.</p></div>" +
        "<div><h3>Henri Grandry</h3>" +
          "<p>Auteur de la traduction wallonne, parue en 2026. Le texte wallon de ce livre lui appartient et est reproduit avec son accord ; il ne peut être repris sans le sien.</p>" +
          "<p>Le bulletin imprime « Henry » en tête d’article et « Henri » sous la colonne wallonne : c’est Henri.</p></div>" +
        "<div><h3>Le lieu</h3>" +
          "<p><b>Xhignez</b> est un hameau de Sprimont, en pays d’Ourthe-Amblève. Un <b>chantoir</b> est une cavité où un ruisseau se perd sous terre — le calcaire de Sprimont en est criblé.</p>" +
          "<p>Le « pus’ » du conte, c’est ce gouffre : son nom wallon de <i>trô d’ chèrpint</i> garde la mémoire de la bête.</p></div>" +
        "<div><h3>Les notes du texte</h3>" +
          D.notes.map(function (n) { return "<p>" + n.n + ". " + n.texte + "</p>"; }).join("") +
          "<p style=\"font-size:13px\">Dans le bulletin, la liste imprimée intervertit les notes 3 et 4 par rapport aux appels du texte. Elles sont rétablies ici en regard de l’appel auquel elles répondent.</p></div>" +
        "<div><h3>Les images</h3>" +
          "<p>Les quatorze planches sont dessinées en SVG, trait et lavis engendrés par le code qui accompagne ce livre. Rien n’est photographié ni emprunté.</p>" +
          "<p>Elles s’animent discrètement — la flamme d’une chandelle, l’œil du serpent, l’éclat des miroirs — et se tiennent tranquilles si votre système demande moins d’animations.</p></div>" +
      "</div>";
    return a;
  }

  /* ------------------------------------------------------------ navigation */
  function va(n, sens) {
    n = Math.max(0, Math.min(total - 1, n));
    if (n === idx && pages.length) return;
    sens = sens || (n > idx ? 1 : -1);
    if (pages[idx]) pages[idx].classList.remove("actuelle", "entre");
    idx = n;
    var p = pages[idx];
    p.style.setProperty("--sens", (sens > 0 ? 26 : -26) + "px");
    p.classList.add("actuelle", "entre");
    p.scrollTop = 0;
    majBarre();
    history.replaceState(null, "", idx === 0 ? location.pathname : "#" + idx);
  }
  function suiv() { va(idx + 1, 1); }
  function prec() { va(idx - 1, -1); }

  var bPrec, bSuiv, parcouru, tete;
  function majBarre() {
    var t = total > 1 ? idx / (total - 1) : 0;
    parcouru.style.width = (t * 100) + "%";
    tete.style.left = (t * 100) + "%";
    bPrec.disabled = idx === 0;
    bSuiv.disabled = idx === total - 1;
  }

  /* ------------------------------------------------------------- montage */
  function monter() {
    pages.push(couverture());
    P.forEach(function (p) { pages.push(pageConte(p)); });
    pages.push(colophon());
    pages.forEach(function (p) { livre.appendChild(p); });

    bPrec = document.getElementById("prec");
    bSuiv = document.getElementById("suiv");
    parcouru = document.getElementById("parcouru");
    tete = document.getElementById("tete");
    bPrec.addEventListener("click", prec);
    bSuiv.addEventListener("click", suiv);
    document.querySelector(".zone.prec").addEventListener("click", prec);
    document.querySelector(".zone.suiv").addEventListener("click", suiv);

    document.querySelectorAll(".idiomes button").forEach(function (b) {
      b.addEventListener("click", function () {
        var v = b.dataset.langue;
        document.body.dataset.langue = v;
        try { localStorage.setItem("langue", v); } catch (e) {}
        document.querySelectorAll(".idiomes button").forEach(function (o) {
          o.setAttribute("aria-pressed", String(o === b));
        });
      });
    });
    var mem = null;
    try { mem = localStorage.getItem("langue"); } catch (e) {}
    var bt = document.querySelector('.idiomes button[data-langue="' + (mem || "deux") + '"]');
    if (bt) bt.click();

    document.addEventListener("keydown", function (e) {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") { e.preventDefault(); suiv(); }
      else if (e.key === "ArrowLeft" || e.key === "PageUp") { e.preventDefault(); prec(); }
      else if (e.key === "Home") { e.preventDefault(); va(0); }
      else if (e.key === "End") { e.preventDefault(); va(total - 1); }
    });

    var x0 = null, y0 = null;
    livre.addEventListener("touchstart", function (e) {
      x0 = e.touches[0].clientX; y0 = e.touches[0].clientY;
    }, { passive: true });
    livre.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
      if (Math.abs(dx) > 56 && Math.abs(dx) > Math.abs(dy) * 1.6) { dx < 0 ? suiv() : prec(); }
      x0 = y0 = null;
    }, { passive: true });

    var d = parseInt((location.hash || "").slice(1), 10);
    va(isNaN(d) ? 0 : d, 1);
  }

  document.readyState === "loading"
    ? document.addEventListener("DOMContentLoaded", monter) : monter();
})();
