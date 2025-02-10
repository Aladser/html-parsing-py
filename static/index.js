// список игр: название=>DOM
let game_names_list = {};
document.querySelectorAll('.game-name').forEach(game => game_names_list[game.textContent] = game);
let games_list = Array.from(document.querySelectorAll('.game'));

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
            for(let key in game_names_list) {
                if(!key.toLowerCase().includes(search_word)) {
                    game_names_list[key].closest('tr').classList.add('d-none');
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

// выбор числа показываемых игр
document.querySelector('#game-count-select').onchange = e => {
    let selected_count = e.target.options[e.target.selectedIndex].value == 'all' ? games_list.length : e.target.options[e.target.selectedIndex].value;
    let games_count = selected_count > games_list.length ? games_list.length : selected_count;
    hideAllGames()
    for (let i=0; i<games_count; i++) {
        games_list[i].classList.remove('d-none');
    }
}

// кнопка наверх
document.querySelector('#scroll-to-btn').onclick = e => window.scrollTo(0, 0);

function showAllGames() {
    for(let key in games_list) {
        games_list[key].classList.remove('d-none');
    }
}
function hideAllGames() {
    for(let key in games_list) {
        games_list[key].classList.add('d-none');
    }
}
