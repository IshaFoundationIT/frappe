from typing import Optional

from pypika.functions import DistinctOptionFunction
from pypika.utils import builder

import frappe


class GROUP_CONCAT(DistinctOptionFunction):
	def __init__(self, column: str, alias: Optional[str] = None):
		"""[ Implements the group concat function read more about it at https://www.geeksforgeeks.org/mysql-group_concat-function ]
		Args:
			column (str): [ name of the column you want to concat]
			alias (Optional[str], optional): [ is this an alias? ]. Defaults to None.
		"""
		super(GROUP_CONCAT, self).__init__("GROUP_CONCAT", column, alias=alias)


class STRING_AGG(DistinctOptionFunction):
	def __init__(self, column: str, separator: str = ",", alias: Optional[str] = None):
		"""[ Implements the group concat function read more about it at https://docs.microsoft.com/en-us/sql/t-sql/functions/string-agg-transact-sql?view=sql-server-ver15 ]

		Args:
			column (str): [ name of the column you want to concat ]
			separator (str, optional): [separator to be used]. Defaults to ",".
			alias (Optional[str], optional): [description]. Defaults to None.
		"""
		super(STRING_AGG, self).__init__("STRING_AGG", column, separator, alias=alias)


class MATCH(DistinctOptionFunction):
	def __init__(self, column: str, *args, **kwargs):
		"""[ Implementation of Match Against read more about it https://dev.mysql.com/doc/refman/8.0/en/fulltext-search.html#function_match ]

		Args:
			column (str):[ column to search in ]
		"""
		alias = kwargs.get("alias")
		super(MATCH, self).__init__(" MATCH", column, *args, alias=alias)
		self._Against = False

	def get_function_sql(self, **kwargs):
		s = super(DistinctOptionFunction, self).get_function_sql(**kwargs)

		if self._Against:
			return f"{s} AGAINST ({frappe.db.escape(f'+{self._Against}*')} IN BOOLEAN MODE)"
		return s

	@builder
	def Against(self, text: str):
		"""[ Text that has to be searched against ]

		Args:
			text (str): [ the text string that we match it against ]
		"""
		self._Against = text


class TO_TSVECTOR(DistinctOptionFunction):
	def __init__(self, column: str, *args, **kwargs):
		"""[ Implementation of TO_TSVECTOR read more about it https://www.postgresql.org/docs/9.1/textsearch-controls.html]

		Args:
			column (str): [ column to search in ]
		"""
		alias = kwargs.get("alias")
		super(TO_TSVECTOR, self).__init__("TO_TSVECTOR", column, *args, alias=alias)
		self._PLAINTO_TSQUERY = False

	def get_function_sql(self, **kwargs):
		s = super(DistinctOptionFunction, self).get_function_sql(**kwargs)
		if self._PLAINTO_TSQUERY:
			return f"{s} @@ PLAINTO_TSQUERY({frappe.db.escape(self._PLAINTO_TSQUERY)})"
		return s

	@builder
	def Against(self, text: str):
		"""[ Text that has to be searched against ]

		Args:
			text (str): [ the text string that we match it against ]
		"""
		self._PLAINTO_TSQUERY = text
