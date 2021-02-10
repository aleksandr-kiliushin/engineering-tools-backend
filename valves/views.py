from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse

from .models import Equipment
from .serializers import EquipmentSerializer

from .utils.create_cp import create_cp



class EquipmentView(APIView):
    def get(self, request):
        cv_valves         = Equipment.objects.filter(equip_type='cv_valve').order_by('id')
        pr_valves         = Equipment.objects.filter(equip_type='pr_valve').order_by('id')
        cv_actuators      = Equipment.objects.filter(equip_type='cv_actuator').order_by('id')
        downstream_blocks = Equipment.objects.filter(equip_type='downstream_block').order_by('id')
        dpr_blocks        = Equipment.objects.filter(equip_type='dpr_block').order_by('id')
        upstream_blocks   = Equipment.objects.filter(equip_type='upstream_block').order_by('id')
        pulse_tubes       = Equipment.objects.filter(equip_type='pulse_tube').order_by('id')
        # the many param informs the serializer that it will be serializing more than a single article.
        cv_valves_serializer         = EquipmentSerializer(cv_valves,         many=True)
        pr_valves_serializer         = EquipmentSerializer(pr_valves,         many=True)
        cv_actuators_serializer      = EquipmentSerializer(cv_actuators,      many=True)
        downstream_blocks_serializer = EquipmentSerializer(downstream_blocks, many=True)
        dpr_blocks_serializer        = EquipmentSerializer(dpr_blocks,        many=True)
        upstream_blocks_serializer   = EquipmentSerializer(upstream_blocks,   many=True)
        pulse_tubes_serializer       = EquipmentSerializer(pulse_tubes,       many=True)

        return Response({
            'cv_valves'         : cv_valves_serializer.data,
            'pr_valves'         : pr_valves_serializer.data,
            'cv_actuators'      : cv_actuators_serializer.data,
            'downstream_blocks' : downstream_blocks_serializer.data,
            'dpr_blocks'        : dpr_blocks_serializer.data,
            'upstream_blocks'   : upstream_blocks_serializer.data,
            'pulse_tubes'       : pulse_tubes_serializer.data,
        })


class DownloadCpView(APIView):
    def post(self, request):

        # Define CP data dictionary of pulse tube.
        pulse_tube_queryset = Equipment.objects.get(code='003G1391')
        pulse_tube_db_data = EquipmentSerializer(pulse_tube_queryset).data
        pulse_tube_cp_data = {}
        for key in pulse_tube_db_data:
            pulse_tube_cp_data[key] = pulse_tube_db_data[key]


        # For received codes, take querysets from DB...
        codes = request.data
        codes_querysets = []
        for code in codes:
            codes_querysets.append(Equipment.objects.get(code=code))
        
        # ... and serialize them to an ordered dict.
        codes_data = EquipmentSerializer(codes_querysets, many=True).data


        # Create an empty cp_data array, ...
        cp_data = []

        # ... populate it with data based on each received code, with amount of 1, ...
        for codes_data_item in codes_data:
            cp_data_item = {}
            for key in codes_data_item:
                cp_data_item[key] = codes_data_item[key]
                cp_data_item['amount'] = 1

            cp_data.append(cp_data_item)

            # ... and, if necessary, add 1 or 2 pulse tubes.
            if (cp_data_item['equip_type'] in ['downstream_block', 'upstream_block', 'dpr_block',]):
                new_pulse_tube_cp_data = pulse_tube_cp_data.copy()
                new_pulse_tube_cp_data['amount'] = 2 if cp_data_item['equip_type'] == 'dpr_block' else 1
                cp_data.append(new_pulse_tube_cp_data)


        # Create "files/cp.xlsx" file, based on codes_data.
        create_cp(cp_data)


        # Confugure the FileResponse and send it to the client.
        response = FileResponse(open('files/cp.xlsx', 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="cp.xlsx"'
        return response
