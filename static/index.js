// список игр: название=>DOM
let games_list = {};
document.querySelectorAll('.game-name').forEach(game => {
    games_list[game.textContent] = game;
});

// поиск игр
let search_input = document.querySelector('#search-input');
if(search_input) {
    search_input.oninput = () => {
        let search_word = search_input.value.toLowerCase();
        if(search_word == '') {
            showAllGames();
            clear_search_btn.classList.add('d-none');
        } else {
            // фраза
            clear_search_btn.classList.remove('d-none');
            for(let key in games_list) {
                if(!key.toLowerCase().includes(search_word)) {
                    games_list[key].closest('tr').classList.add('d-none');
                }
            }
        }
    };    
}

// очистка поля поиска
let clear_search_btn = document.querySelector('#clear-search-btn');
if(clear_search_btn) {
    clear_search_btn.onclick = () => {
        search_input.value = "";
        showAllGames()
    }
}

function showAllGames() {
    for(let key in games_list) {
        games_list[key].closest('tr').classList.remove('d-none');
    }
}
