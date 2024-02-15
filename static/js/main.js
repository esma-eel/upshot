//Django basic setup for accepting ajax requests.
// Cookie obtainer Django

var data = null;
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
// Setup ajax connections safetly
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function clean_messages() {
    setTimeout(function () {
        if ($(".alert").is(":visible")) {
            $(".alert").fadeOut("fast");
        }
    }, 4000)
}

function comment_edit_ajax_function(elem, url) {
    var return_data = "";
    var url_togo = url
    $.ajax({
        url: url_togo,
        async: false,
        data: {
            'id': $(elem).data('id'),
            'action': $(elem).data('action'),
            'body': $(elem).data('body'),
            'active': $(elem).data('active'),
        },
        dataType: 'json',
        type: 'POST',
        success: function (data) {
            return_data = data;
        }
    });
    return return_data;
}

function ajax_function(elem, url) {
    var return_data = "";
    var url_togo = url
    $.ajax({
        url: url_togo,
        async: false,
        data: {
            'id': $(elem).data('id'),
            'action': $(elem).data('action')
        },
        dataType: 'json',
        type: 'POST',
        success: function (data) {
            return_data = data;
        }
    });
    return return_data;
}



function comment_delete_comments_managemnt(elem) {
    data = ajax_function(elem, '/account/ajax/comment_actions/')
    data_to_work = {
        'id': $(elem).data('id'),
        'action': $(elem).data('action')
    }

    if (data.status == "ok") {
        
        if (data_to_work.action == "delete_comment") {
            var comment_row = $('#comment_' + data_to_work.id + '_row');
            var comment_action_modal = $("#delete_comment_modal" + data_to_work.id);
            var message_container = $("#message_container");
            
            comment_action_modal.modal('hide');

            comment_row.hide();
            comment_row.remove();

            message_container.append('<li class="alert alert-success alert-dismissible">' + data.message + '<button type="button" class="close" data-dismiss="alert">&times;</button></li>')
            clean_messages();
        }
    } else {
        console.table(data);
    }
}

function edit_comment_body_function(elem) {
    data_to_work = {
        'id': $(elem).data('id'),
        'action': $(elem).data('action'),
        'body': $(elem).data('body'),
        
    };
    url = '/account/ajax/comment_actions/';
    var comment_action_modal = $("#edit_comment_modal" + data_to_work.id);
    var message_container = $("#message_container");
    var new_body= $("#new_body"+$(elem).data('id')).val();

    if (data_to_work.body != new_body) {
        $(elem).data('body', new_body);
        data_to_work.body  = $(elem).data('body');
        data = comment_edit_ajax_function(elem, url);

        if (data.status == 'ok') {
            comment_body_in_table = $('#comment_body_in_table'+data_to_work.id);
            comment_body_in_table.text(data_to_work.body.substring(0, 25)+'...');
            new_body.val = data_to_work.body
            
            message_container.append('<li class="alert alert-success alert-dismissible">' + data.message + '<button type="button" class="close" data-dismiss="alert">&times;</button></li>');

            clean_messages()

        } else {
            console.log("pew")
        }

        comment_action_modal.modal('hide');
    } else {
        comment_action_modal.modal('hide');
    }

    
}

function edit_comment_active_function(elem) {
  
    var message_container = $("#message_container");

    if ($(elem).data('active') == "True") {
        $(elem).text("غیرفعال");
        $(elem).data('active', "False");
        $(elem).attr('data-active', "False");
        $(elem).removeClass('badge-success');
        $(elem).addClass('badge-danger');
    } else {
        $(elem).text("فعال");
        $(elem).data('active', "True");
        $(elem).attr('data-active', "True");
        $(elem).removeClass('badge-danger');
        $(elem).addClass('badge-success');
    }
    url = '/account/ajax/comment_actions/'
    data = comment_edit_ajax_function(elem, url);

    if (data.status == "ok") {
        message_container.append('<li class="alert alert-success alert-dismissible">' + data.message + '<button type="button" class="close" data-dismiss="alert">&times;</button></li>');

        clean_messages();
    } else {
        console.log("pew!")
    }
}


function article_delete_articles_managemnt(elem) {
    data = ajax_function(elem, '/account/ajax/article_actions/')
    data_to_work = {
        'id': $(elem).data('id'),
        'action': $(elem).data('action')
    }

    if (data.status == "ok") {
        
        if (data_to_work.action == "delete_article") {
            var article_row = $('#article_' + data_to_work.id + '_row');
            var article_action_modal = $("#delete_article_modal" + data_to_work.id);
            var message_container = $("#message_container");
            article_action_modal.modal('hide')

            article_row.hide();
            article_row.remove();

            message_container.append('<li class="alert alert-success alert-dismissible">' + data.message + '<button type="button" class="close" data-dismiss="alert">&times;</button></li>')

            clean_messages()
        }
    } else {
        console.table(data);
    }
}


function follower_delete_followers_managemnt(elem) {
    data = ajax_function(elem, '/account/ajax/follow_unfollow/')
    data_to_work = {
        'id': $(elem).data('id'),
        'action': $(elem).data('action')
    }
    if (data.status == "ok") {
        
        if (data_to_work.action == "delete_follower") {
            var user_row = $('#follower_' + data_to_work.id + '_row');
            var user_unfollow_modal = $("#delete_follower_modal" + data_to_work.id);
            var message_container = $("#message_container");
            user_unfollow_modal.modal('hide')

            user_row.hide();
            user_row.remove();

            message_container.append('<li class="alert alert-success alert-dismissible">' + data.message + '<button type="button" class="close" data-dismiss="alert">&times;</button></li>')

            clean_messages()
        }

        if (data_to_work.action == "delete_following") {
            var user_row = $('#following_' + data_to_work.id + '_row');
            var user_unfollow_modal = $("#delete_following_modal" + data_to_work.id);
            var message_container = $("#message_container");
            user_unfollow_modal.modal('hide')

            user_row.hide();
            user_row.remove();

            message_container.append('<li class="alert alert-success alert-dismissible">' + data.message + '<button type="button" class="close" data-dismiss="alert">&times;</button></li>')

            clean_messages()
        }

    } else {
        console.log("pew!");
    }
}

function follower_delete_profile(elem) {
    data = ajax_function(elem, '/account/ajax/follow_unfollow/')
    data_to_work = {
        'id': $(elem).data('id'),
        'action': $(elem).data('action')
    }
    
    if (data.status == "ok") {
        
        var follower_status_badge = $('#follower_status_badge');
        var user_unfollow_modal = $("#delete_follower_modal" + data_to_work.id);
        var message_container = $("#message_container");
        var delete_from_follower_triger = $('#delete_from_follower_triger');
        user_unfollow_modal.modal('hide');

        follower_status_badge.text('شما را دنبال نمیکند');

        message_container.append('<li class="alert alert-success alert-dismissible">' + data.message + '<button type="button" class="close" data-dismiss="alert">&times;</button></li>');
        delete_from_follower_triger.remove();

        clean_messages()

    } else {
        console.log("pew!");
    }
}

function follow_unfollow_user_function(elem) {
    
    data = ajax_function(elem, '/account/ajax/follow_unfollow/')
    data_to_work = {
        'id': $(elem).data('id'),
        'action': $(elem).data('action')
    }
    
    if (data.status == "ok") {
        
        var follow_status_badge = $('#follow_status_badge');
        var message_container = $("#message_container");


        var prev_action = data_to_work.action;
        //toggle data action
        $(elem).data('action', prev_action == 'follow_user' ? 'unfollow_user' : 'follow_user')
        // toggle link text
        $(elem).text(prev_action == "follow_user" ? 'دنبال نکردن' : 'دنبال کردن')
        // follow status badge
        follow_status_badge.text(prev_action == "follow_user" ? 'دنبال میکنید' : 'دنبال نمیکنید')


        // new_action = $(elem).data('action')
        message_container.append('<li class="alert alert-success alert-dismissible">' + data.message + '<button type="button" class="close" data-dismiss="alert">&times;</button></li>');

        clean_messages()


    } else {
        console.log("pew!");
    }
}

// vote voting
function user_voting_function(elem, e) {
    e.preventDefault();
    data_to_work = {
        'id': $(elem).data('id'),
        'action': $(elem).data('action'),
        'user_already_voted_neg': $(elem).data('user-already-voted-neg'),
        'user_already_voted_pos': $(elem).data('user-already-voted-pos'),
    }
    
    data = ajax_function(elem, '/article/ajax/vote_actions/');
    
    
    if (data.status == "ok") {
        var negative_counter = $(".negative-counter");
        var positive_counter = $(".positive-counter");
        
        if (data_to_work.action == "positive_vote" && (!data_to_work.user_already_voted_pos)) {
            var old_pos_count = parseInt(positive_counter.text());
            var new_pos_count = old_pos_count + 1;
            positive_counter.text(new_pos_count);

            var old_neg_count = parseInt(negative_counter.text());
            var new_neg_count = old_neg_count - 1;
            new_neg_count = new_neg_count > 0 ? new_neg_count:0;
            negative_counter.text(new_neg_count);

            $(elem).data('user-already-voted-pos', true);
            $('#vote-neg-holder').data('user-already-voted-neg', false);
        }

        if (data_to_work.action == "negative_vote" && (!data_to_work.user_already_voted_neg)) {
            var old_neg_count = parseInt(negative_counter.text());
            var new_neg_count = old_neg_count + 1;
            negative_counter.text(new_neg_count);

            var old_pos_count = parseInt(positive_counter.text());
            var new_pos_count = old_pos_count - 1;
            new_pos_count = new_pos_count > 0 ? new_pos_count:0;
            positive_counter.text(new_pos_count);

            $('#vote-pos-holder').data('user-already-voted-pos', false);
            $(elem).data('user-already-voted-neg', true);
            
        }
        

    } else {
        console.log("pew!");
    }
}

// request
function st_request_delete_st_request_managemnt(elem) {
    data = ajax_function(elem, '/account/ajax/mentor_request_actions/')
    data_to_work = {
        'id': $(elem).data('id'),
        'action': $(elem).data('action')
    }
    
    if (data.status == "ok") {
        
        var request_row = $('#st_request' + data_to_work.id + '_row');
        var request_delete_modal = $("#delete_st_request_modal" + data_to_work.id);
        var message_container = $("#message_container");
        request_delete_modal.modal('hide')

        request_row.hide();
        request_row.remove();

        message_container.append('<li class="alert alert-success alert-dismissible">' + data.message + '<button type="button" class="close" data-dismiss="alert">&times;</button></li>')

        clean_messages()

    } else {
        console.log("pew!");
    }
}


function st_request_accept_reject_request_managemnt(elem) {
    data = ajax_function(elem, '/account/ajax/mentor_request_actions/')
    data_to_work = {
        'id': $(elem).data('id'),
        'action': $(elem).data('action')
    };

    var status_badge = $('#st_request_mentor_status_badge'+data_to_work.id);

    if (status_badge.data('active') == "True") {
        if (data_to_work.action == "mentor_reject_request") {
            status_badge.text("قبول نشده");
            status_badge.data('active', "False");
            status_badge.attr('data-active', "False");
            status_badge.removeClass('badge-info');
            status_badge.addClass('badge-warning');
        }
    } else {
        if (data_to_work.action == "mentor_accept_request") {
            status_badge.text("قبول شده");
            status_badge.data('active', "True");
            status_badge.attr('data-active', "True");
            status_badge.removeClass('badge-warning');
            status_badge.addClass('badge-info');
        }
    }
    
    if (data.status == "ok") {
        var message_container = $("#message_container");

        if (data_to_work.action == "mentor_accept_request") {
            $('#mentor_request_accept_button'+data_to_work.id).attr('disabled', "true");
        } else {
            $('#mentor_request_accept_button'+data_to_work.id).removeAttr('disabled');
        }

        if (data_to_work.action == "mentor_reject_request") {
            $('#mentor_request_reject_button'+data_to_work.id).attr('disabled', "true");
        } else {
            $('#mentor_request_reject_button'+data_to_work.id).removeAttr('disabled');
        }

        message_container.append('<li class="alert alert-success alert-dismissible">' + data.message + '<button type="button" class="close" data-dismiss="alert">&times;</button></li>');

        clean_messages();

    } else {
        console.log("pew!");
    }
}

function send_mentor_request_to_user(elem) {
    data = ajax_function(elem, '/account/ajax/mentor_request_actions/')
    data_to_work = {
        'id': $(elem).data('id'),
        'action': $(elem).data('action')
    };

    if (data.status == "ok") {
        var message_container = $("#message_container");

        $(elem).text('درخواست ارسال شد');
        $(elem).removeAttr('onclick');

        message_container.append('<li class="alert alert-success alert-dismissible">' + data.message + '<button type="button" class="close" data-dismiss="alert">&times;</button></li>');

        clean_messages();
    } else {
        console.log("pew!")
    }
}

function send_mentor_request_to_user_profile(elem) {
    data = ajax_function(elem, '/account/ajax/mentor_request_actions/')
    data_to_work = {
        'id': $(elem).data('id'),
        'action': $(elem).data('action')
    };

    if (data.status == "ok") {
        var message_container = $("#message_container");

        var profile_manage_request_button = $('#profile-manage-request-button');

        $(elem).removeAttr('onclick');
        $(elem).removeAttr('data-id');
        $(elem).removeAttr('data-action');
        
        $(elem).text('مدیریت درخواست های ارسالی')
        $(elem).addClass('d-none');
        $(elem).remove();
        profile_manage_request_button.removeClass('d-none');
        profile_manage_request_button.addClass('d-block');


        message_container.append('<li class="alert alert-success alert-dismissible">' + data.message + '<button type="button" class="close" data-dismiss="alert">&times;</button></li>');

        clean_messages();
    } else {
        console.log("pew!")
    }
}



// main jq functinon
$(function () {
    clean_messages();
    article_body_container_imgs = $('#article_body_container > p > img').addClass('img-fluid');
    
    $('[data-toggle="tooltip"]').tooltip();

    var owl = $('.owl-carousel');
    owl.owlCarousel({
        loop: true,
        responsiveClass: true,
        rtl:true,
        autoHeight:false,
        nav: true,
        autoplay:true,
        autoplayTimeout:3500,
        autoplayHoverPause:true,
        navText: ['<i class="fas fa-angle-right"></i>', '<i class="fas fa-angle-left"></i>'],
        responsive: {
          0: {
            items: 1,        
          },
          600: {
            items: 1,        
          },
          1000: {
            items: 4,            
            margin: 20
          }
        }
      });

    // $('.my-hover-acc').hover(function(e) {
    //     // over
    //     $(this).next().collapse('show');
    // }, function(e) {
    //     // out
    //     $(this).next().collapse('hide');
    // });
      
});
// for data table
$(function() {
    var mydatatable = $('.my-table-management')
    mydatatable.DataTable({
    ajax: data,
    deferRender: true,
    scrollY:     500,
    scroller:    true,
    language: {
        processing:     "درحال انجام کار ...",
        search:         " جستجو: ",
        lengthMenu:    "تعداد نمایش:  _MENU_  سطر ",
        info:           "نمایش سطر های   _START_ تا _END_ از _TOTAL_ سطر",
        infoEmpty:      "نمایش سطر های   0 تا 0 از 0 سطر",
        infoFiltered:   "(در مجموع از _MAX_ مورد فیلتر شده است)",
        infoPostFix:    "",
        loadingRecords: "بارگزاری سطر ها",
        zeroRecords:    "هیچ سطری وجود ندارد",
        emptyTable:     "جدول خالی میباشد",
        paginate: {
            first:      "اولین",
            previous:   "قبلی",
            next:       "بعدی",
            last:       "آخرین"
        },
        aria: {
            sortAscending:  ": برای مرتب سازی ستون به ترتیب صعودی فعال کنید",
            sortDescending: ": برای مرتب سازی ستون به ترتیب نزولی فعال کنید"
            }
        }
    });

    $('div.dataTables_filter input').addClass('form-control p-2 rounded-pill');

});