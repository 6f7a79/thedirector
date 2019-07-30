import unicodedata


class Misc:

    def isAdm(self, user_id, admin_list):
        for adm in admin_list:
            admid = adm.user.id
            if admid == user_id:
                return True
        return False

    def isArabic(self, first_name):
        for letter in first_name:
            try:
                encoding = unicodedata.name(letter).lower()
                if 'arabic' in encoding or 'persian' in encoding:
                    return True
            except ValueError:
                pass
        return False

    def parserEntities(self, entities, post):
        titlechk = False
        urlchk = False
        title = ''
        url = ''
        hashtags = []

        for entity in entities:
            if entity.type == "hashtag":
                offset = entity.offset
                length = offset + entity.length
                hashtags.append(post[offset:length])

            elif entity.type == "bold" and not titlechk:
                titlechk = True
                offset = entity.offset
                length = offset + entity.length
                title = post[offset:length]

            elif entity.type == "url" and not urlchk:
                urlchk = True
                offset = entity.offset
                length = offset + entity.length
                url = post[offset:length]

        if not titlechk or not urlchk:
            return False

        response = {"hashtags": hashtags, "title": title, "url": url}
        return response
