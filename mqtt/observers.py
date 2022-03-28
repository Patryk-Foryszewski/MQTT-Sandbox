from events import Subject, Observer
import logging

logger = logging.getLogger(__name__)


class StickerStatusObserver(Observer):

    def update(self, subject: Subject) -> None:
        text = str(subject.message.payload.decode('utf-8'))
        if 'DAMAGED' in text:
            logger.exception("ENCOUNTERED DAMAGED STICKER")
