/* 数字ピンイン → 声調記号つきピンイン（出典の数字表記から生成） */
(function (g) {
  'use strict';
  var MARKS = {
    a: ['ā', 'á', 'ǎ', 'à'], e: ['ē', 'é', 'ě', 'è'], i: ['ī', 'í', 'ǐ', 'ì'],
    o: ['ō', 'ó', 'ǒ', 'ò'], u: ['ū', 'ú', 'ǔ', 'ù'], 'ü': ['ǖ', 'ǘ', 'ǚ', 'ǜ']
  };
  function split(num) {
    return num.trim().toLowerCase().split(/\s+/).map(function (s) {
      var m = s.match(/^([a-zü:v]+)([0-5]?)$/);
      if (!m) throw new Error('bad pinyin syllable: ' + s);
      return { base: m[1].replace(/u:|v/g, 'ü'), tone: m[2] === '' ? 5 : +m[2] };
    });
  }
  function markSyl(base, tone) {
    if (tone < 1 || tone > 4) return base;
    var idx = -1;
    if (base.indexOf('a') >= 0) idx = base.indexOf('a');
    else if (base.indexOf('e') >= 0) idx = base.indexOf('e');
    else if (base.indexOf('ou') >= 0) idx = base.indexOf('o');
    else {
      for (var i = base.length - 1; i >= 0; i--) { if ('iouü'.indexOf(base[i]) >= 0) { idx = i; break; } }
    }
    if (idx < 0) return base;
    return base.slice(0, idx) + MARKS[base[idx]][tone - 1] + base.slice(idx + 1);
  }
  function join(parts) {
    return parts.map(function (p, i) { return (i > 0 && /^[aeo]/.test(p.plain)) ? "'" + p.txt : p.txt; }).join('');
  }
  function render(sylls, cap) {
    var s = join(sylls.map(function (x) { return { txt: markSyl(x.base, x.tone), plain: x.base }; }));
    return cap ? s.charAt(0).toUpperCase() + s.slice(1) : s;
  }
  function plain(sylls, cap) {
    var s = join(sylls.map(function (x) { return { txt: x.base, plain: x.base }; }));
    return cap ? s.charAt(0).toUpperCase() + s.slice(1) : s;
  }
  g.Pinyin = { split: split, markSyl: markSyl, render: render, plain: plain };
})(window);
