import logging
from dataclasses import dataclass, field
from typing import List, Optional
import json
import yaml
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Node:
    data: List[str] = field(default_factory=list)  # 数据项的列表
    parent: Optional['Node'] = None  # 父项
    children: List['Node'] = field(default_factory=list)  # 子项的列表

    def addChild(self, child: 'Node', data_name='data', parent_name='parent', children_name='children') -> None:
        """添加子项"""
        child.parent = self
        if data_name:
            setattr(child, data_name, child.data)
        if parent_name:
            setattr(child, parent_name, child.parent)
        if children_name:
            setattr(child, children_name, child.children)
        self.children.append(child)
        logger.info(f"+ {child.data}")
        logger.info(f"{'  ' * (len(self.children) - 1)}|")
        logger.info(f"{'  ' * (len(self.children) - 1)}+--")

    def child(self, row: int) -> 'Node':
        """获取指定行的子项"""
        return self.children[row]

    def childCount(self) -> int:
        """获取子项数量"""
        return len(self.children)

    def columnCount(self) -> int:
        """获取列数"""
        return len(self.data)

    def data(self, column: int) -> str:
        """获取指定列的数据"""
        if column < 0 or column >= len(self.data):
            return None
        return self.data[column]

    def parent(self) -> Optional['Node']:
        """获取父项"""
        return self.parent

    def row(self) -> int:
        """获取行数"""
        if self.parent is not None:
            return self.parent.children.index(self)
        return 0

    def to_dict(self, data_name='data', parent_name='parent', children_name='children') -> dict:
        """将对象转换为字典"""
        d = {
            data_name: self.data,
            children_name: [c.to_dict(data_name, parent_name, children_name) for c in self.children],
        }
        if self.parent is not None:
            d[parent_name] = self.parent.to_dict(data_name, parent_name, children_name)
        return d

    @classmethod
    def from_dict(cls, d: dict, data_name='data', parent_name='parent', children_name='children') -> 'Node':
        """从字典中创建对象"""
        item = cls()
        if hasattr(d, '__getitem__'):
            if data_name in d:
                item.data = d[data_name]
            for child in d[children_name]:
                item.addChild(cls.from_dict(child, data_name, parent_name, children_name))
            if parent_name in d and d[parent_name] is not None:
                item.parent = cls.from_dict(d[parent_name], data_name, parent_name, children_name)
        return item

    def to_json(self, data_name='data', parent_name='parent', children_name='children') -> str:
        """将对象转换为JSON字符串"""
        return json.dumps(self.to_dict(data_name, parent_name, children_name))

    @classmethod
    def from_json(cls, json_str: str, data_name='data', parent_name='parent', children_name='children') -> 'Node':
        """从JSON字符串中创建对象"""
        return cls.from_dict(json.loads(json_str), data_name, parent_name, children_name)

    def to_yaml(self, data_name='data', parent_name='parent', children_name='children') -> str:
        """将对象转换为YAML字符串"""
        return yaml.dump(self.to_dict(data_name, parent_name, children_name), default_flow_style=False)

    @classmethod
    def from_yaml(cls, yaml_str: str, data_name='data', parent_name='parent', children_name='children') -> 'Node':
        """从YAML字符串中创建对象"""
        return cls.from_dict(yaml.safe_load(yaml_str))

    def to_xml(self) -> str:
        """将对象转换为XML字符串"""
        elem = ET.Element('item')
        if self.data:
            ET.SubElement(elem, 'data').text = ','.join(self.data)
        for child in self.children:
            elem.append(child.to_xml())
        if self.parent is not None:
            elem.append(self.parent.to_xml())
        return ET.tostring(elem, encoding='unicode')

    @classmethod
    def from_xml(cls, xml_str: str) -> 'Node':
        """从XML字符串中创建对象"""
        elem = ET.fromstring(xml_str)
        item = cls(elem.find('data').text.split(','))
        for child_elem in elem.findall('item'):
            item.addChild(cls.from_xml(str(ET.tostring(child_elem))))
        if elem.find('parent') is not None:
            item.parent = cls.from_xml(str(ET.tostring(elem.find('parent'))))
        return item

