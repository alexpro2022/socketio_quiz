var store = {
  topic: {},
  game: {},

};

app_pages = {
    topics:  {},
    entering: {},
    searching: {},
    playing: {},
    results: {},
    disconnected: {}
}

document.addEventListener('DOMContentLoaded', function () {

    app = new Lariska({
      store: store,
      container: "#app",
      pages: app_pages,
      url: window.location.hostname
    });
    app.on("connect", null, ()=> {app.emit("get_topics")})

    // Когда загружены темы, переходим на страницу выбора темы
    app.on("topics", "#topics", (data)=>{
        app.store.topics=data
    })

    // Когда игра пришла, обновляем ее
    app.on("game", null, (data)=>{
        console.log(data)
        app.store.game = data
        app.go("playing")
    })

    app.addHandler("feedback", (data)=> {
        answer = data.answer - 1
        console.log(`Выделяем ответ ${answer}`)
        option_element = document.querySelectorAll(".questions_option")[answer]
        option_element.classList.add("correct_option");

    })

    // Обрабатываем нажатие назад
    app.addHandler("back", ()=> {app.go("topics") } )

    // Клиент выбирает тему
    app.addHandler("pick_topic", (topic)=> {
        app.store.topic = topic
        console.log(app.store.topic)
        app.go("entering")
    } )

    // Клиент присоединяется к игре
    app.addHandler("join", ()=> {
         playerName = document.getElementById("player_name").value
         app.emit("join_game", {topic_pk: app.store.topic.pk, name: playerName})
         app.go("searching")
    } )

    app.addHandler("answer", (index)=> {
        app.emit("answer", {index: index+1, game_uid: app.store.game.uid})
        // console.log(app.store.game.uid)
        console.log(`Выделяем ответ ${index}`)
        option_element = document.querySelectorAll(".questions_option")[index]
        option_element.classList.add("selected_option");
    })

   app.on("disconnect", "#disconnect")

})
