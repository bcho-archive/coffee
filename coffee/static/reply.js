$('a.reply').click(function(e) {
    e.preventDefault();

    var comment_id = $(this).attr('data-comment-id');
    var comment_author = $(this).attr('data-comment-author');
    $('#compose-new textarea').focus().val('@' + comment_author + ' ');
    $('#compose-new').attr('action', '/comment/' + comment_id + '/reply');
});
