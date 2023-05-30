function fetch_result() {
    let input = document.getElementById('search-input').value;
    let url = document.getElementById('search-form').getAttribute('data-url');
    window.location.href = url + '?name=' + input;
}

window.onload = function () {
    input = document.getElementById('search-input')
    input.focus();
    let val = this.input.value;
    this.input.value = '';
    this.input.value = val;
};