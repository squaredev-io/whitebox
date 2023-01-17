/* mathjax-loader.js  file */
/* ref: http://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/ */
(function (win, doc) {
    win.MathJax = {
      config: ["MMLorHTML.js"],
      extensions: ["tex2jax.js"],
      jax: ["input/TeX"],
      tex2jax: {
        inlineMath: [ ["\\(","\\)"] ],
        displayMath: [ ["\\[","\\]"] ]
      },
      TeX: {
        TagSide: "right",
        TagIndent: ".8em",
        MultLineWidth: "85%",
        equationNumbers: {
          autoNumber: "AMS",
        },
        unicode: {
          fonts: "STIXGeneral,'Arial Unicode MS'"
        }
      },
      displayAlign: 'center',
      showProcessingMessages: false,
      messageStyle: 'none'
    };
  })(window, document);