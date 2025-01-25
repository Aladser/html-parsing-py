// список игр: название=>DOM игры
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
            // пустое поле
            for(let key in games_list) {
                games_list[key].closest('tr').classList.remove('d-none');
            }
        } else {
            // фраза
            for(let key in games_list) {
                if(!key.toLowerCase().includes(search_word)) {
                    games_list[key].closest('tr').classList.add('d-none');
                }
            }
        }
    };    
}
