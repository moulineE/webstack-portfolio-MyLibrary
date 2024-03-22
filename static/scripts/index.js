$(document).ready(function () {
  $(':input').on('input', async function () {
    const input = $(this);
    if (input.val() === '') {
      $('.booksResult').html('');
      return;
    }
    const response = await fetch('/mylibrary/api/v1/search?q=' + input.val());
    const books = await response.json();
    console.log(books);
    let html = '';
    for (const book of books) {
      let author = (await fetch('/mylibrary/api/v1/authors/' + book.author_id));
      author = await author.json();
      html += `<li><a style="text-decoration:none" href="/mylibrary/book?id=${book.id}"><h2> ${book.book_title}</h2><h3>${author.first_name + ' ' + author.last_name}</h3><h4>published the ${book.published_date}</h4><p>${book.book_summary}</p></a></li>`;
    }
    $('UL.booksResult').html(html);
  });
});
