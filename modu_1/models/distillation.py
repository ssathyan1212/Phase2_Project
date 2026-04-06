# models/distillation.py
import torch.nn.functional as F
def distillation_loss(student_pred, teacher_pred, alpha=0.7):
    l_pred = F.mse_loss(student_pred, teacher_pred.detach())
    return alpha * l_pred
