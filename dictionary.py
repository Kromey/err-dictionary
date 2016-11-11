import requests


from errbot import BotPlugin, botcmd


class Dictionary(BotPlugin):
    """
    Leveraging the Wordnik API, this plugin allows you to look up definitions,
    synonyms, and more for English words.
    """

    def activate(self):
        if not self.config:
            # Don't allow activation until we're configured
            self.log.info('Dictionary is not configured, forbidding activation')
            return

        return super().activate()

    def get_configuration_template(self):
        return {
                'WORDNIK_API_KEY': '00112233445566778899aabbccddeeffgg',
                }

    _define_api = 'http://api.wordnik.com/v4/word.json/{word}/definitions?limit=5&includeRelated=true&useCanonical=true&includeTags=false&api_key={API_KEY}'
    @botcmd
    def define(self, msg, args):
        """
        Define a word
        """
        results = requests.get(
                self._define_api.format(
                    word=args,
                    API_KEY=self.config['WORDNIK_API_KEY'])
                ).json()

        if not results:
            return "I couldn't find anything for that."

        resp = []
        for result in results:
            line = "{:d}: {}".format(
                    int(result['sequence'])+1,
                    result['text'],
                    )
            resp.append(line)

        return "\n".join(resp)

