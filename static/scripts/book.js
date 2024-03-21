$(document).ready(function () {
  $('#addBookmarkBtn').click(function () {
    const bookmarkName = prompt('Please enter a bookmark name:');
    if (bookmarkName != null) {
      const currentPage = $(this).data('page');
      const bookId = $(this).data('book-id');
      const userId = $(this).data('user-id');
      $.ajax({
        url: '/mylibrary/api/v1/bookmarks',
        type: 'POST',
        data: {
          bookmark_name: bookmarkName,
          page: currentPage,
          book_id: bookId,
          user_id: userId
        },
        success: function (result) {
          alert('Bookmark added successfully!');
          $('#getBookmarksBtn').click();
        },
        error: function (error) {
          console.error(error);
          alert('Failed to add bookmark. Error: ' + error.responseText);
        }
      });
    }
  });
  $('#getBookmarksBtn').click(function () {
    const bookId = $(this).data('book-id');
    const userId = $(this).data('user-id');
    $.ajax({
      url: '/mylibrary/api/v1/bookmarks?book_id=' + bookId + '&user_id=' + userId,
      type: 'GET',
      success: function (result) {
        let html = '';
        for (const bookmark of result) {
          html += `<p><a href="/mylibrary/book?id=${bookmark.book_id}&page=${bookmark.page}">${bookmark.bookmark_name}</a> <button class="deleteBookmarkBtn" data-bookmark-id="${bookmark.id}">X</button></p>`;
        }
        $('#bookmarksContainer').html(html);
      },
      error: function (error) {
        console.error(error);
        alert('Failed to retrieve bookmarks. Please try again.');
      }
    });
  });
  $('#bookmarksContainer').on('click', '.deleteBookmarkBtn', function () {
    const bookmarkId = $(this).data('bookmark-id');
    $.ajax({
      url: '/mylibrary/api/v1/bookmarks/' + bookmarkId,
      type: 'DELETE',
      success: function (result) {
        alert('Bookmark deleted successfully!');
        $('#getBookmarksBtn').click();
      },
      error: function (error) {
        console.error(error);
        alert('Failed to delete bookmark. Please try again.');
      }
    });
  });
});
