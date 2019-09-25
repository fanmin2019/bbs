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

var apiTodoAdd = function(form, callback) {
    var path = '/blog/api/update_title'
    ajax('POST', path, form, callback)
}

var apiTodoDelete = function(form, callback) {
    var path = '/blog/api/delete'
    ajax('POST', path, form, callback)
}

var bindDeleteEvent = function () {
    var delete_btn = document.getElementById("id-delete-btn")
    delete_btn.onclick = function(event) {
        if(window.confirm("Are you sure?")) {
            var id = e('input[name="id"]').value
            log("id", id)
            var form = {
                id: id
            }
            apiTodoDelete(form, function(res) {
                alert(res.message)
                location.href = "/"
            })

        }

    }

}

var __main = function () {
    // markContents()
    // registerTimer()
    // highlight()
    bindUpdateEvent()
    bindDeleteEvent()

    var title = e('.topic_full_title')
    title.addEventListener('blur', function () {
       log("edit end")
        var title = e('.topic_full_title').innerText
        log('click add', title)
        var id = e('input[name="id"]').value
        log("id", id)
        var form = {
            id: id,
            title: title,
        }
        apiTodoAdd(form, function(todo) {
            // 收到返回的数据, 插入到页面中
            //insertTodo(todo)
            console.log(todo)
        })

    })
}


__main()
