from .models import Message


class Chat:
    def __init__(self, first_user, second_user):
        sent = list(Message.objects.filter(to=first_user, user=second_user))
        received = list(Message.objects.filter(to=second_user, user=first_user))
        i, j = 0, 0
        self.messages = []
        while i < len(sent) or j < len(received):
            if i < len(sent) and j < len(received) and sent[i].id < received[j].id:
                self.messages.append(sent[i])
                i += 1
            elif i < len(sent) and j < len(received) and sent[i].id > received[j].id:
                self.messages.append(received[j])
                j += 1
            elif i < len(sent) and j == len(received):
                self.messages += sent[i:]
                break
            elif j < len(received) and i == len(sent):
                self.messages += received[j:]
                break

    def list_of_messages(self):
        return self.messages

    def get_last_message(self):
        return self.messages[-1]
