from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

# запросы для теста
# Добавление альбома
# http -f POST http://localhost:8081/albums artist="Test" genre="Rock" album="Super" year="2018"
# Запрос албома артистов
# http localhost:8081/albums/Test

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Всего альбомов {}. Список альбомов {}: ".format(len(albums_list), artist)
        result += ", ".join(album_names)
    return result

@route("/albums", method="POST")
def albumsadd():
    curAlbum = {"year": request.forms.get("year"), "artist": request.forms.get("artist"), "genre": request.forms.get("genre"), "album": request.forms.get("album")}
    validateResult = album.validate(curAlbum)
    if validateResult != "":
        return HTTPError(409, validateResult)
    findAlbum = album.findFirst(curAlbum["artist"], curAlbum["album"], curAlbum["year"])    

    if findAlbum != None:
        message = "Альбом уже существует"
        return HTTPError(409, message)
    else:
        albumAdd=album.new(curAlbum)
        return "Данные успешно сохранены "

if __name__ == "__main__":
    run(host="localhost", port=8081, debug=True)
