function filterCards(num) {
    var divsToHideA = document.getElementsByName("available-card");
    var divsToHideR = document.getElementsByName("requested-card");
    var divsToHideL = document.getElementsByName("loaned-card");
    if (num == 1) {
        var divsToHide = [...divsToHideR, ...divsToHideL];
        var divsToShow = divsToHideA;
    }
    else if (num == 2) {
        var divsToHide = [...divsToHideA, ...divsToHideL];
        var divsToShow = divsToHideR;
    }
    else if (num == 3) {
        var divsToHide = [...divsToHideA, ...divsToHideR];
        var divsToShow = divsToHideL;
    }
    else {
        var divsToHide = [];
        var divsToShow = [];
        divsToShow.push(...divsToHideA);
        divsToShow.push(...divsToHideR);
        divsToShow.push(...divsToHideL);
    }
    for (var i = 0; i < divsToHide.length; i++) {
        divsToHide[i].style.opacity = 0.3;
        console.log('hide '+ i);

    }
    for (var i = 0; i < divsToShow.length; i++) {
        divsToShow[i].style.opacity = 1;
        console.log('show' + i);

    }
    return divsToShow;   // The function returns the product of p1 and p2
}