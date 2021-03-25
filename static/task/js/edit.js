
// // to save changes
// save_tag_name_changes();


// $(".editing_input").keypress(function (e) {
//     if(e.keyCode == 13 || e.key == "Enter"){
//         save_tag_name_changes();
//     }
// });

// // $("#editing_input").

// $("#editing_input").focus();
// $("#editing_input").select();
var editing_currently = null;
var action_call = true;

$(".editinginput-icon").on("click", function () {
    let clicked_id = this.id;
    let container = clicked_id.split("-");
    let type = container[1];
    let id = container[2];
    let focused_text_p = `#text-${type}-${id}`;
    let focused_input = `#editinginput-${type}-${id}`;
    $(focused_input).val($(focused_text_p).text().trim());
    $(focused_text_p).hide();
    $(focused_input).show();
    $(focused_input).focus();
    $(focused_input).select();
    editing_currently = {
        'type': type,
        'id': id
    }
});

$(".editinginput-icon").keypress(function (e) {
    if(e.keyCode == 13 || e.key == "Enter"){
        save_changes();
        action_call = false;
    }
});

function save_changes() {
    if (action_call) {    
        if (editing_currently) {
            let focused_text_p = `#text-${editing_currently.type}-${editing_currently.id}`;
            let focused_input = `#editinginput-${editing_currently.type}-${editing_currently.id}`;
            let new_text = $(focused_input).val();
            editing_currently.new_text = new_text;

            $.ajax({
                url: "/editText",
                type: "GET",
                data: editing_currently,
                success: (response)=>{
                    console.log(response);
                    if (response.status) {
                        $(focused_text_p).text(response.new_text);
                    }
                    $(focused_text_p).show();
                    $(focused_input).hide();
                }
            });
        }
    }else{
        action_call = true;
    }
}


