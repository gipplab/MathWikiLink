function makeMyTool() {
  function isEquation(formula){
    const equation_symbols = ["=","neq","leq","geq",">","<"];
    if (equation_symbols.some(symbol => formula.includes(symbol)))
        return true;
    return false;
  }
  function getRequest(url,formula,callback) {

    var xhr = new XMLHttpRequest();

    xhr.open('GET', url, true);

    xhr.onload = function() {

      if (xhr.status === 200) {
        callback(xhr.responseText,formula);
      } else {

      }

    }
    xhr.send();
  }

  function processResponse(response, formula) {

    const myObj = JSON.parse(response);
    var ou = $(".latex-dialog-options-panel").first();
    var disp = "{\\displaystyle "+formula+"}";
    console.log(disp);
    if(isEquation(formula)){
      var reccomendation = myObj[disp]["name"]; 
      var qid = myObj[disp]["qid"]; 
      ou.append(`<div><h4>Name,             QID </h4> <p> ${reccomendation}                 ${qid}  </p> `);
    }
    else{
      var recommendation_sources = myObj[formula];
      for (var i = 0; i < recommendation_sources.length; i++) {
        for (var recommendation_index = 0; recommendation_index < 3; recommendation_index++) { 
          if(recommendation_sources[i][Object.keys(recommendation_sources[i])].length > recommendation_index){
            console.log(recommendation_index);
            var reccomendation =  recommendation_sources[i][Object.keys(recommendation_sources[i])][recommendation_index]["name"];
            var qid = recommendation_sources[i][Object.keys(recommendation_sources[i])][recommendation_index]["qid"];  
            //console.log(reccomendation);
            ou.append(`<div><h4>Name,             QID </h4> <p> ${reccomendation}                 ${qid}  </p> `);
          }
        }
      }
    }
  }
  var formula = document.getElementsByClassName("latex-dialog-formula-field")[0].getElementsByTagName("textarea")[0];
  if(isEquation(formula.value)){
      var url = "https://raw.githubusercontent.com/gipplab/MathWikiLink/master/dataset/formula_string_index.json"}
  else {
    var url = "https://raw.githubusercontent.com/gipplab/MathWikiLink/master/backend/annomathtex/recommendation/evaluation_files/identifier_index.json"}
  getRequest(url,formula.value,processResponse);
}

function _asyncToGenerator(fn) {
  return function() {
    var gen = fn.apply(this, arguments);
    return new Promise(function(resolve, reject) {
      function step(key, arg) {
        try {
          var info = gen[key](arg);
          var value = info.value;
        } catch (error) {
          reject(error);
          return;
        }
        if (info.done) {
          resolve(value);
        } else {
          return Promise.resolve(value).then(function(value) {
            return step("next", value);
          }, function(err) {
            return step("throw", err);
          });
        }
      }
      return step("next");
    });
  };
}

mw.hook('ve.ui.MwLatexDialogReady').add( makeMyTool);
