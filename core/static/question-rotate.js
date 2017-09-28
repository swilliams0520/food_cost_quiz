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
        // index = (index >= 0) ? index % $images.length : $images.length + index;
        // Hide the last visible item.
        $images.eq($this.attr('current-image')).removeClass('gallerify-show');
        // Update our current position by distance.
        $images.eq(index).addClass('gallerify-show');
        // Set the current image data.
        $this.attr('current-image', index);
    }

    var $nextButton = $('<button id="arrow-button-next" />').text('next question');
    var $prevButton = $('<button id="arrow-button-previous" />').text('previous question');

    $this.append($prevButton);
    $this.append($nextButton);

    function removeButtons() {
      if($this.attr('current-image') === ($images.length - 1).toString()) {
        $('#arrow-button-next').prop("disabled", true);
        $('#quiz-submit').show();
      } else {
        $('#quiz-submit').hide();
        $('#arrow-button-next').removeAttr("disabled");
      }

      if (parseInt($this.attr('current-image')) === 0) {
        $('#arrow-button-previous').prop("disabled", true);
      } else {
        $('#arrow-button-previous').removeAttr("disabled");
      }

    }

    removeButtons();

    $nextButton.click(function(e) {
        e.preventDefault();
        moveAroundGallery(1);
        removeButtons();
        return false;
    });
    $prevButton.click(function(e) {
        e.preventDefault();
        moveAroundGallery(-1);
        removeButtons();
        return false;

    });
    // testing hide next button at last question

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
