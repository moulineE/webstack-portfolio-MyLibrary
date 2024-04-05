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
      let author = (await fetch('/mylibrary/api/v1/authors_by_book/' + book.book_id));
      author = await author.json();
      let lang = (await fetch('/mylibrary/api/v1/languages_by_id/' + book.language_id));
      lang = await lang.json();
      let publish = '';
      if (lang == 'en') {
    publish = 'published the'
      } else {
    publish = 'publié le'
      }
      if (lang == 'fr' && book.language_id == 'ca9669f2-1908-4c8c-b3ce-38bdb2d04b62') {
              html += `<li><a style="text-decoration:none" href="/mylibrary/book?id=${book.book_id}&lang=${lang}"><h2> ${book.book_title}</h2><h3>${author.first_name + ' ' + author.last_name}</h3><h4>${publish} ${book.published_date}</h4><p>${book.book_summary}</p></a></li>`;
      }
    }
    $('UL.booksResult').html(html);
  });
});
