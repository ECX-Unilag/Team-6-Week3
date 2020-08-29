$(".toggle-password").click(function () {

    $(this).toggleClass("fa-eye fa-eye-slash");
    var input = $($(this).attr("toggle"));
    if (input.attr("type") == "password") {
        input.attr("type", "text");
    } else {
        input.attr("type", "password");
    }
});
$(".toggle-password2").click(function () {

    $(this).toggleClass("fa-eye fa-eye-slash");
    var input2 = $('#password-field2');
    if (input2.attr("type") == "password") {
        input2.attr("type", "text");
    } else {
        input2.attr("type", "password");
    }
});
$(document).ready(function () {

    $('.owl-carousel').owlCarousel({
        loop: true,
        margin: 20,
        nav: true,
        autoplay: true,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 3
            }
        }
    })
});

window.addEventListener('load', function () {
    const loader = document.querySelector('.loader');
    loader.classList.add('done');

});