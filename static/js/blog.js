var e = function (sel) {
    return document.querySelector(sel)
}

var es = function (sel) {
    return document.querySelectorAll(sel)
}

var markContents = function () {
    var contentDivs = es('.markdown-text')
    for (var i = 0; i < contentDivs.length; i++) {
        var contentDiv = contentDivs[i]
        var content = marked(contentDiv.textContent)
        // console.log(content, contentDiv.innerHTML)
        contentDiv.innerHTML = content
    }
}


var highlight = function () {
    var code_list = es('pre code')
    for (var i = 0; i < code_list.length; i++) {
        var code = code_list[i]
        code.className = code.className.replace('lang', 'language')
    }
}

var registerTimer = function () {
    setInterval(function () {
        var times = es('.min-time')
        for (var i = 0; i < times.length; i++) {
            var t = times[i]
            var time = Number(t.id)
            var now = Math.floor(new Date() / 1000)
            var delta = now - time
            var s = `秒前 ${delta}`
            t.innerText = s
        }
    }, 1000)
}

var bindUpdateEvent = function () {
    var edit_btn = document.getElementById("id-edit-btn")
        edit_btn.onclick = function (event) {
            console.log("clicked")
            document.getElementById("id-markdown-text").style.display = 'none'
            document.getElementById("id-edit-text").style.display = 'block'
            document.getElementById("id-edit-btn").style.display = 'none'
            document.getElementById("id-delete-btn").style.display = 'none'
            document.getElementById("id-update-btn").style.display = 'block'

        }
}

var __main = function () {
    // markContents()
    // registerTimer()
    // highlight()
    bindUpdateEvent()
}


__main()
