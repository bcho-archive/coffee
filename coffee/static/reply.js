$('a.reply').click(function(e) {
    e.preventDefault();
    var comment_id = $(this).attr('data-comment-id');
    $('#compose-new textarea').focus().val('@游客 ');
    $('#compose-new').attr('action', '/comment/' + comment_id + '/reply');
});
