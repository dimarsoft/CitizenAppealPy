import aiohttp


async def send(url: str, name: str, email: str, message: str) -> dict:
    """
    Отправка обращения
    :param url: Куда, АПИ
    :param name: Имя
    :param email: Почта
    :param message: Сообщение
    :return:
        Ответ от сервера
    """

    headers = {"Content-Type": "application/json"}
    data = {
        "name": name,
        "email": email,
        "message": message
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                response_json = await response.json()
    except Exception as ex:
        print(ex)
        return {"error": str(ex)}

    print(response_json)
    return response_json
