$.fn.gallerify = function(opts) {
    opts = opts || {}; // Options.
    var $this = this; // Keep our current scope.

    // Default image to display.
    var defaultImage = opts.defaultImage || 0;
    $this.attr('current-image', defaultImage);

    // Get the image tags inside the div...
    var $images = $this.children('div');
    // Show our default image.
    $images.eq($this.attr('current-image')).addClass('gallerify-show');
    // Give our images ids.
    $images.each(function(index, image) {
        $(image).attr('gallery-index', index);
    });

    // Move around our gallery by distance.
    function moveAroundGallery(distance) {
        // Wrap our current index to map our images.
        var index = parseInt($this.attr('current-image')) + distance;
        // Fancy math to make sure we're not wrapping negatively.
        index = (index >= 0) ? index % $images.length : $images.length + index;
        // Hide the last visible item.
        $images.eq($this.attr('current-image')).removeClass('gallerify-show');
        // Update our current position by distance.
        $images.eq(index).addClass('gallerify-show');
        // Set the current image data.
        $this.attr('current-image', index);
    }

    var $nextButton = $('<button id="arrow-button" />').text('next question');
    var $prevButton = $('<button id-"arrow-button" />').text('previous question');

    $this.append($prevButton);
    $this.append($nextButton)

    $nextButton.click(function(e) {
        e.preventDefault();
        moveAroundGallery(1);
        return false;
    });
    $prevButton.click(function(e) {
        e.preventDefault();
        moveAroundGallery(-1);
        return false;
    })
};

// Bind our plugin to tags that have our image-gallery attribute.
$(document).ready(function() {
    // Append a custom style to the page for us to use.
    $('<style />')
        .text('[gallerify] > div:not(.gallerify-show) { display: none; }')
        .appendTo(document.head);

    // Traverse the dom and setup our plugin on
    // all divs with the gallerify attribute.
    $('[gallerify]').each(function(index, gallery) {
        $(this).gallerify();
    });
});
