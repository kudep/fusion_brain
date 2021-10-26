from typing import Dict

from .state_schema import Bot, BotUtterance, Dialog, Human, HumanUtterance


class StateManager:
    def __init__(self, *args, **kwargs):
        pass

    async def add_human_utterance(self, dialog: Dialog, payload: Dict, label: str, **kwargs) -> None:
        dialog.add_human_utterance()
        dialog.utterances[-1].text = payload
        dialog.utterances[-1].user = dialog.human.to_dict()
        dialog.utterances[-1].attributes = kwargs.get("message_attrs", {})

    async def add_hypothesis(self, dialog: Dialog, payload: Dict, label: str, **kwargs):
        hypothesis = {"skill_name": label, "annotations": {}}
        for h in payload:
            dialog.utterances[-1].hypotheses.append({**hypothesis, **h})

    async def add_annotation(self, dialog: Dialog, payload: Dict, label: str, **kwargs):
        dialog.utterances[-1].annotations[label] = payload

    async def add_annotation_prev_bot_utt(self, dialog: Dialog, payload: Dict, label: str, **kwargs):
        if len(dialog.utterances) > 1:
            dialog.utterances[-2].annotations[label] = payload
            dialog.utterances[-2].actual = False

    async def add_hypothesis_annotation(self, dialog: Dialog, payload: Dict, label: str, **kwargs):
        ind = kwargs["ind"]
        dialog.utterances[-1].hypotheses[ind]["annotations"][label] = payload

    async def add_hypothesis_annotation_batch(self, dialog: Dialog, payload: Dict, label: str, **kwargs):
        if isinstance(dialog.utterances[-1], BotUtterance):
            return
        if len(dialog.utterances[-1].hypotheses) != len(payload["batch"]):
            for i in range(len(dialog.utterances[-1].hypotheses)):
                dialog.utterances[-1].hypotheses[i]["annotations"][label] = {}
        else:
            for i in range(len(payload["batch"])):
                dialog.utterances[-1].hypotheses[i]["annotations"][label] = payload["batch"][i]

    async def add_text(self, dialog: Dialog, payload: str, label: str, **kwargs):
        dialog.utterances[-1].text = payload

    async def update_human(self, human: Human, active_skill: Dict):
        attributes = active_skill.get("human_attributes", {})
        for attr_name, attr_value in attributes.items():
            if attr_name in human.to_dict():
                setattr(human, attr_name, attr_value)
            elif attr_name in human.profile:
                human.profile[attr_name] = attr_value
            else:
                human.attributes[attr_name] = attr_value

    async def update_bot(self, bot: Bot, active_skill: Dict):
        attributes = active_skill.get("bot_attributes", {})
        for attr_name, attr_value in attributes.items():
            if attr_name in bot.to_dict():
                setattr(bot, attr_name, attr_value)
            else:
                bot.attributes[attr_name] = attr_value

    async def add_bot_utterance(self, dialog: Dialog, payload: Dict, label: str, **kwargs) -> None:
        await self.update_human(dialog.human, payload)
        await self.update_bot(dialog.bot, payload)
        dialog.add_bot_utterance()
        dialog.utterances[-1].text = payload["text"]
        dialog.utterances[-1].orig_text = payload["text"]
        dialog.utterances[-1].active_skill = payload["skill_name"]
        dialog.utterances[-1].confidence = payload["confidence"]
        dialog.utterances[-1].annotations = payload.get("annotations", {})
        dialog.utterances[-1].user = dialog.bot.to_dict()

    async def add_bot_utterance_last_chance(self, dialog: Dialog, payload: Dict, label: str, **kwargs) -> None:
        if isinstance(dialog.utterances[-1], HumanUtterance):
            dialog.add_bot_utterance()
            dialog.utterances[-1].text = payload["text"]
            dialog.utterances[-1].orig_text = payload["text"]
            dialog.utterances[-1].active_skill = label
            dialog.utterances[-1].confidence = 0
            dialog.utterances[-1].annotations = payload["annotations"]
            dialog.utterances[-1].user = dialog.bot.to_dict()

    async def add_bot_utterance_last_chance_overwrite(
        self, dialog: Dialog, payload: Dict, label: str, **kwargs
    ) -> None:
        if isinstance(dialog.utterances[-1], HumanUtterance):
            dialog.add_bot_utterance()
        dialog.utterances[-1].text = payload["text"]
        dialog.utterances[-1].orig_text = payload["text"]
        dialog.utterances[-1].active_skill = label
        dialog.utterances[-1].confidence = 0
        dialog.utterances[-1].annotations = payload["annotations"]
        dialog.utterances[-1].user = dialog.bot.to_dict()

    async def add_failure_bot_utterance(self, dialog: Dialog, payload: Dict, label: str, **kwargs) -> None:
        dialog.add_bot_utterance()
        dialog.utterances[-1].text = payload
        dialog.utterances[-1].orig_text = payload
        dialog.utterances[-1].active_skill = label
        dialog.utterances[-1].confidence = 0
        dialog.utterances[-1].user = dialog.bot.to_dict()

    async def save_dialog(self, dialog: Dialog, payload: Dict, label: str, **kwargs) -> None:
        pass

    async def get_or_create_dialog(self, user_external_id, channel_type, **kwargs):
        human = Human(external_id=user_external_id)
        dialog_obj = Dialog(_human_id=human._id, human=human, channel_type=channel_type)
        dialog_obj.bot = Bot()
        return dialog_obj

    async def get_dialog_by_id(self, dialog_id):
        return []

    async def get_dialog_by_dialog_id(self, dialog_id):
        return []

    async def list_dialog_ids(self, *args, **kwargs):
        return []

    async def get_dialogs_by_user_ext_id(self, user_external_id):
        return []

    async def get_all_dialogs(self):
        return []

    async def drop_active_dialog(self, user_external_id):
        pass

    async def set_rating_dialog(self, user_external_id, dialog_id, rating):
        pass

    async def set_rating_utterance(self, user_external_id, utt_id, rating):
        pass

    async def drop_and_rating_active_dialog(self, user_external_id, rating):
        pass

    async def prepare_db(self):
        pass

    async def get_channels(self):
        return []
