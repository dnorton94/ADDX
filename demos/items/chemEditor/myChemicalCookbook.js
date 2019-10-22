    var chemEditor;
    var chemComposer;
    function init()
    {
      /*
      var elem = document.getElementById('chemComposer');
      var chemEditor = new Kekule.Editor.ChemSpaceEditor(document, null, Kekule.Render.RendererType.R2D);
      chemComposer = new Kekule.Editor.Composer(elem, chemEditor);
      */
      chemComposer = Kekule.Widget.getWidgetById('chemComposer');
      chemComposer
        .setEnableDimensionTransform(true)
        .setAutoSetMinDimension(true)
        .setAutoResizeConstraints({width: 1, height: 1})
        .autoResizeToClient();  // force a resize to window client
    }
    Kekule.X.domReady(init);