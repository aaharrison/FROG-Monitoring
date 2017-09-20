function renderViz() {
    try {
        var placeholderDiv = document.getElementById("holder");
        var url = "https://10az.online.tableau.com/t/roundhouseonemkthink/views/FROGStory/FROG?:embed=y&:showAppBanner=false&:showShareOptions=true&:display_count=no&:showVizHome=no";
        var options = {
            width: window.innerWidth - 15,
            height: window.innerHeight,
            hideTabs: true,
            hideToolbar: true,
            onFirstInteractive: function () {
                workbook = viz.getWorkbook();
                activeSheet = workbook.getActiveSheet();
                console.log("API Connecting")}
            }    
        viz = new tableau.Viz(placeholderDiv, url, options)
    }

    catch(err) {
        viz.dispose()
        var placeholderDiv = document.getElementById("holder");
        var url = "https://10az.online.tableau.com/t/roundhouseonemkthink/views/FROGStory/FROG?:embed=y&:showAppBanner=false&:showShareOptions=true&:display_count=no&:showVizHome=no";
        var options = {
            width: window.innerWidth - 15,
            height: window.innerHeight,
            hideTabs: true,
            hideToolbar: true,
            onFirstInteractive: function () {
                workbook = viz.getWorkbook();
                activeSheet = workbook.getActiveSheet();
                console.log("API Connecting After Resize")}
            }    
        viz = new tableau.Viz(placeholderDiv, url, options)
    }
};

function openRH1() {
    window.open("https://www.roundhouseone.com")
}


