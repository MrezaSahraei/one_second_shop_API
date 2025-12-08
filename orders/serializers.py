from rest_framework import serializers
from .models import OrderItems, Order

class OrderSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    pay_way_display = serializers.CharField(source='get_pay_way_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'orderer', 'phone', 'first_name', 'last_name', 'address',
                  'province', 'city', 'postal_code', 'status', 'pay_way',
                  'is_paid', 'for_me', 'status_display','pay_way_display' ,'created_at', 'updated_at'
                  ]
        read_only_fields = ['id', 'orderer', 'status', 'is_paid', 'created_at', 'updated_at', 'pay_way']

    def validate_postal_code(self,value):
        if value and not len(value) == 15:
            raise serializers.ValidationError('کد پستی باید 15 رقم باشد')
        if value and not value.isdigit():
            raise serializers.ValidationError('کد پستی وارد شده باید عددی باشد')
        return value

    def validate_address(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('حداقل حروف ادرس نباید از 10 کمتر باشد')
        return value

    def validate_phone(self, value):
        if value and not len(value) == 11:
            raise serializers.ValidationError('شماره موبایل باید 11 رقم داشته باشد')
        if value and not value.isdigit:
            raise serializers.ValidationError('شماره موبایل وارد شده باید عددی باشد')
        if value and not value.startswith('09'):
            raise serializers.ValidationError('شماره موبایل وارد شده باید با 09 شروع شود')


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['id', 'order', 'product', 'quantity', 'price_now']
        read_only_fields = ['id', 'price_now']