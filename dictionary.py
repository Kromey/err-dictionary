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
    @botcmd(split_args_with=None)
    def define(self, msg, args):
        """
        Define a word
        """
        word = args[0]

        results = requests.get(
                self._define_api.format(
                    word=word,
                    API_KEY=self.config['WORDNIK_API_KEY'])
                ).json()

        if not results:
            return "I couldn't find anything for that."

        resp = []
        # Canonicalize word
        word = results[0]['word']
        last_source = results[0]['attributionText']
        seq = 0
        last_type = ''
        for result in results:
            seq += 1
            if result['partOfSpeech'] != last_type:
                last_type = result['partOfSpeech']
                resp.append("{}, {}:".format(
                    word,
                    last_type))

            line = "{:d}: {}".format(
                    seq,
                    result['text'],
                    )
            resp.append(line)

            # Make sure we cite dictionaries properly
            if result['attributionText'] != last_source:
                resp.append(last_source)
                last_source = result['attributionText']

        # Make sure we cite the last dictionary in our results as well
        resp.append(last_source)
        # Attribute to Wordnik
        resp.append("Powered by Wordnik -- https://www.wordnik.com/words/{word}".format(word=word))

        return "\n".join(resp)

