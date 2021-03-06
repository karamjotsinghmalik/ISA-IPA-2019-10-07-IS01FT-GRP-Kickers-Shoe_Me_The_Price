var shoe_data = {
    'Nike Air Max': null,
    'Nike Vapormax': null,
    'Nike Jordan Mars 270 ': null,
    'Adidas Superstar ': null,
    'Nike Nike Joyride': null,
    'Champion Zone 93': null,
    'Nike Air Force 1 Low': null,
    'Nike Tuned 1': null,
    'Nike Air Force 1 Mid': null,
    'Adidas Stan Smith': null,
    'Asics Gel Kayano': null,
    'Reebok Superflex V2': null,
    'Asics Gel Quantum Jcq 360': null,
    'Nike Air Max Plus Deconstructed': null,
    'Nike Legacy 312': null,
    'Diadora Rebound Ace': null,
    'Diadora Action': null,
    'Diadora Game Low': null,
    'Nike Spizike': null
}
var selected_data = [];
$(document).ready(function () {
    $('.carousel').carousel({
        noWrap: false,
        indicators: true
    });

    $('.chips-placeholder').chips({
    placeholder: 'E.g Nike Air Max 1',
    secondaryPlaceholder: '+Tag',
  });
    $('.chips-autocomplete').chips({
        autocompleteOptions: {
            data: shoe_data,
            limit: Infinity,
            minLength: 1,
            placeholder: 'E.g Nike Zoom Freak 1'
        },
        onChipAdd: function (e, chip) {
            shoe = chip.innerHTML.substr(0, chip.innerHTML.indexOf("<i"));
            selected_data.push(shoe);
            document.getElementById('sn').value = selected_data;
        },
        onChipDelete: function (e, chip) {
            shoe = chip.innerHTML.substr(0, chip.innerHTML.indexOf("<i"));

        }
    });
    $('select').formSelect();
});
