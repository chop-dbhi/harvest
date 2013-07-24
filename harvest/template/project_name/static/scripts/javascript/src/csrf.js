define(['cilantro'], function(c) {

    function sameOrigin(url) {
        var host = document.location.host,
            protocol = document.location.protocol,
            srOrigin = '//' + host,
            origin = protocol + srOrigin;

        return (url === origin || url.slice(0, origin.length + 1) === origin + '/') || (url === srOrigin || url.slice(0, srOrigin.length + 1) === srOrigin + '/') || !(/^(\/\/|http:|https:).*/.test(url));
    };

    function safeMethod(method) {
        return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    };

    $.ajaxPrefilter(function(settings, origSettings, xhr) {
        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            return xhr.setRequestHeader('X-CSRFToken', window.csrf_token);
        }
    });

});
