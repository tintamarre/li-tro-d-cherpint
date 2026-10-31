/* « Li trô d' chèrpint » — on tourne les pages au clic, comme un feuillet. */
(function () {
  "use strict";
  var D = window.LIVRE, M = D.meta, P = D.pages, NOTES = {}, GLOS = D.glossaire || {};
  D.notes.forEach(function (n) { NOTES[String(n.n)] = n.texte; });

  var livre = document.getElementById("pages"),
      total = P.length + 2,            // couverture + 13 pages + colophon
      idx = -1, pages = [];   // -1 : aucune page montee, sinon va(0) sortirait aussitot

  /* ------------------------------------------------- gloser le vocabulaire */
  /* Les mots difficiles du français et les appels de note s'expliquent au
     survol, pour qu'un enfant puisse lire sans buter. */
  var RE = null;
  (function () {
    var mots = Object.keys(GLOS).sort(function (a, b) { return b.length - a.length; });
    if (!mots.length) return;
    var motif = "(?<![\\w\\u00C0-\\u024F])(" +
        mots.map(function (m) { return m.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }).join("|") +
        ")(?![\\w\\u00C0-\\u024F])";
    try { RE = new RegExp(motif, "giu"); } catch (e) { RE = null; }   // lookbehind absent : on s'en passe
  })();

  function gloser(p) {
    p.querySelectorAll("sup[data-note]").forEach(function (sp) {
      var n = sp.getAttribute("data-note");
      if (!NOTES[n]) return;
      sp.className = "mot appel";
      sp.tabIndex = 0;
      sp.setAttribute("role", "button");
      sp.setAttribute("data-glose", NOTES[n]);
    });
    var cible = p.querySelector(".fr.corps");
    if (!cible || !RE) return;
    var tw = document.createTreeWalker(cible, NodeFilter.SHOW_TEXT, null, false), t, lot = [];
    while ((t = tw.nextNode())) lot.push(t);
    lot.forEach(function (n) {
      var txt = n.nodeValue;
      RE.lastIndex = 0;
      if (!RE.test(txt)) return;
      RE.lastIndex = 0;
      var frag = document.createDocumentFragment(), fin = 0, m;
      while ((m = RE.exec(txt))) {
        if (m.index > fin) frag.appendChild(document.createTextNode(txt.slice(fin, m.index)));
        var b = document.createElement("span");
        b.className = "mot";
        b.tabIndex = 0;
        b.setAttribute("role", "button");
        b.textContent = m[0];
        b.setAttribute("data-glose", GLOS[m[0].toLowerCase()] || "");
        frag.appendChild(b);
        fin = m.index + m[0].length;
      }
      if (fin < txt.length) frag.appendChild(document.createTextNode(txt.slice(fin)));
      n.parentNode.replaceChild(frag, n);
    });
  }

  var bulle, courant = null;
  function montrer(el) {
    var texte = el.getAttribute("data-glose");
    if (!texte) return;
    courant = el;
    bulle.textContent = texte;
    bulle.classList.add("visible");
    var r = el.getBoundingClientRect(), b = bulle.getBoundingClientRect();
    var x = Math.max(12, Math.min(r.left + r.width / 2 - b.width / 2, innerWidth - b.width - 12));
    var dessus = r.top > b.height + 20;
    bulle.style.left = Math.round(x) + "px";
    bulle.style.top = Math.round(dessus ? r.top - b.height - 11 : r.bottom + 11) + "px";
    bulle.classList.toggle("dessous", !dessus);
    bulle.style.setProperty("--fleche", Math.round(r.left + r.width / 2 - x) + "px");
    el.setAttribute("aria-describedby", "glose");
  }
  function cacher() {
    bulle.classList.remove("visible");
    if (courant) courant.removeAttribute("aria-describedby");
    courant = null;
  }

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
        "<div><h3>Les mots difficiles</h3>" +
          "<p>Le français de 1930 ne se laisse pas lire tout seul à huit ans. Les mots soulignés de pointillés — <i>chantoir</i>, <i>fourches patibulaires</i>, <i>occire</i>, <i>miroir aux alouettes</i> — s’expliquent quand on passe la souris dessus, ou qu’on les touche du doigt.</p>" +
          "<p>Les appels de note du texte wallon s’ouvrent de la même façon.</p></div>" +
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
    cacher();
    if (pages[idx]) pages[idx].classList.remove("actuelle", "entre");
    idx = n;
    var p = pages[idx];
    p.style.setProperty("--sens", (sens > 0 ? 26 : -26) + "px");
    p.classList.add("actuelle", "entre");
    p.scrollTop = 0;
    majBarre();
    mesurer();
    history.replaceState(null, "", idx === 0 ? location.pathname : "#" + idx);
  }
  function suiv() { va(idx + 1, 1); }
  function prec() { va(idx - 1, -1); }

  /* L'en-tête et les colonnes de texte se calent sur la largeur réelle de la
     planche, pour que tout s'aligne sur une même justification. */
  function mesurer() {
    var p = pages[idx];
    if (!p) return;
    var img = p.querySelector(".planche img");
    if (!img) { document.documentElement.style.removeProperty("--mesure"); return; }
    var l = img.getBoundingClientRect().width;
    document.documentElement.style.setProperty("--mesure", l > 40 ? Math.round(l) + "px" : "100%");
  }

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
    pages.forEach(function (p) { livre.appendChild(p); gloser(p); });

    bulle = document.createElement("div");
    bulle.className = "glose";
    bulle.id = "glose";
    bulle.setAttribute("role", "tooltip");
    document.body.appendChild(bulle);
    livre.addEventListener("mouseover", function (e) {
      var m = e.target.closest(".mot"); if (m && m !== courant) montrer(m);
    });
    livre.addEventListener("mouseout", function (e) {
      if (e.target.closest(".mot")) cacher();
    });
    livre.addEventListener("focusin", function (e) {
      var m = e.target.closest(".mot"); if (m) montrer(m);
    });
    livre.addEventListener("focusout", cacher);
    livre.addEventListener("click", function (e) {
      var m = e.target.closest(".mot");
      if (!m) return;
      e.stopPropagation();                     // ne pas tourner la page sur un mot
      courant === m ? cacher() : montrer(m);
    });
    addEventListener("keydown", function (e) { if (e.key === "Escape") cacher(); });

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

    addEventListener("resize", mesurer);
    if (window.ResizeObserver) new ResizeObserver(mesurer).observe(livre);
    livre.querySelectorAll(".planche img").forEach(function (im) {
      im.addEventListener("load", mesurer);
    });

    var d = parseInt((location.hash || "").slice(1), 10);
    va(isNaN(d) ? 0 : d, 1);
    setTimeout(mesurer, 120);
  }

  document.readyState === "loading"
    ? document.addEventListener("DOMContentLoaded", monter) : monter();
})();
